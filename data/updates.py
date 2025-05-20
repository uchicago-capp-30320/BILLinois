from data_utils import pull_page, insert_bills
from datetime import date
from datetime import timedelta
import time
import os
import psycopg2
import sys
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(BASE_DIR / ".env")


# Connect to DB, parse state and session from input args
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
state = sys.argv[1]
session = sys.argv[2]

# Set up cursor, and clear updates_table
cur = conn.cursor()
cur.execute("DELETE FROM updates_table;")

# Setting up date, total pages, and number of inserts
today_date = date.today()
since_date = str(today_date - timedelta(days=1))
_, total_pages_updated = pull_page(state, session, 1, since_date)
num_updated_inserts = 0

# Iterate through each page, deleting outdated records if needed,
# inserting updated data, and populating updates table
for p in range(1, total_pages_updated + 1):
    page_updated_bills, _ = pull_page(state, session, p, since_date)
    if not page_updated_bills:
        print("No updates to bills")
        break
    print(f"deleting records from page {p}")
    for record in page_updated_bills:
        id_to_delete = record["id"]

        # NOTE: Cannot delete bills as that would get rid of people's favorites
        sponsors_delete_statement = """DELETE FROM sponsors_table WHERE bill_id = (%s)"""
        actions_delete_statement = """DELETE FROM actions_table WHERE bill_id = (%s)"""
        # NOTE: Re-running topic assignment allows us to use most updated summary/title
        topics_delete_statement = """DELETE FROM topics_table WHERE bill_id = (%s)"""

        # Deleting from actions/sponsors first as PK issue
        cur.execute(actions_delete_statement, (id_to_delete,))
        cur.execute(sponsors_delete_statement, (id_to_delete,))
        cur.execute(topics_delete_statement, (id_to_delete,))

    print(f"inserting updated bills from page {p}")
    all_info_from_page = insert_bills(page_updated_bills)
    # Extract all information from returned dictionary
    updated_bills = all_info_from_page["bills_from_page"]
    updated_sponsors = all_info_from_page["sponsors_from_page"]
    updated_actions = all_info_from_page["actions_from_page"]
    updates = all_info_from_page["updates_from_page"]
    topics = all_info_from_page["topics_from_page"]
    updated_inserts = all_info_from_page["inserts_from_page"]

    arguments_bills_updated = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", bill).decode("utf-8") for bill in updated_bills
    )
    arguments_sponsors_updated = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", sponsor).decode("utf-8")
        for sponsor in updated_sponsors
    )
    arguments_actions_updated = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", action).decode("utf-8")
        for action in updated_actions
    )
    arguments_updates = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", bill_update).decode("utf-8")
        for bill_update in updates
    )
    arguments_topics = ",".join(
        cur.mogrify("(%s, %s)", topic_pair).decode("utf-8") for topic_pair in topics
    )

    cur.execute(
        "INSERT INTO bills_table (bill_id, number, title, summary, status, state, session) VALUES "
        + arguments_bills_updated
        + " ON CONFLICT (bill_id) DO UPDATE SET title=EXCLUDED.title, summary=EXCLUDED.summary, status=EXCLUDED.status;"
    )
    cur.execute(
        """
        INSERT INTO sponsors_table (id, bill_id, sponsor_id, sponsor_name, party, position) VALUES
        """
        + " "
        + arguments_sponsors_updated
    )
    cur.execute(
        """
        INSERT INTO actions_table (action_id, bill_id, description, chamber, date, category) VALUES
        """
        + " "
        + arguments_actions_updated
    )
    if updates:
        cur.execute(
            """
            INSERT INTO updates_table(bill_id, category, description, chamber, action_id, date) VALUES
            """
            + " "
            + arguments_updates
        )

    if topics:
        cur.execute("INSERT INTO topics_table (bill_id, topic) VALUES " + arguments_topics)

    # Committing at every ~5k inserts
    num_updated_inserts += updated_inserts
    if num_updated_inserts >= 5000:
        conn.commit()
        num_updated_inserts = 0
    p += 1
    time.sleep(6)

# Close out
conn.commit()
cur.close()
conn.close()
