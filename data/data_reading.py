"""
This file includes the code to ingestion all of the legislation from the 104th session
"""

import psycopg2
import os
import time
from data_utils import pull_page, insert_bills
import sys
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(BASE_DIR / ".env")

# Setup and unpacking state, session from command line
start = time.time()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
state = sys.argv[1]
session = sys.argv[2]

# Use helper function to get number of pages
_, max_pages = pull_page(state, session, 1)

num_inserts = 0
for i in range(1, max_pages + 1):
    print(f"Pulling bills from page {i}")

    # Helper function runs query to get all bill info from current page
    page_info, _ = pull_page(state, session, i)

    # Storing all info from one page in a list for mass insert
    all_page_info = insert_bills(page_info)
    inserts_on_page = all_page_info["inserts_from_page"]
    num_inserts += inserts_on_page

    # Unpacking dict
    bills = all_page_info["bills_from_page"]
    sponsors = all_page_info["sponsors_from_page"]
    actions = all_page_info["actions_from_page"]
    topics = all_page_info["topics_from_page"]

    # Mass inserting with lists
    arguments_bills = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s, %s)", bill).decode("utf-8") for bill in bills
    )
    arguments_sponsors = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", sponsor).decode("utf-8") for sponsor in sponsors
    )
    arguments_actions = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", action).decode("utf-8") for action in actions
    )
    arguments_topics = ",".join(
        cur.mogrify("(%s, %s)", topic_pair).decode("utf-8") for topic_pair in topics
    )

    cur.execute(
        "INSERT INTO bills_table (bill_id, number, title, summary, status, state, session) VALUES "
        + arguments_bills
    )
    cur.execute(
        """
        INSERT INTO sponsors_table (id, bill_id, sponsor_id, sponsor_name, party, position) VALUES
        """
        + " "
        + arguments_sponsors
    )
    cur.execute(
        """
        INSERT INTO actions_table (action_id, bill_id, description, chamber, date, category) VALUES
        """
        + " "
        + arguments_actions
    )

    if topics:
        cur.execute("INSERT INTO topics_table (bill_id, topic) VALUES " + arguments_topics)

    # Committing after ~5,000 inserts, moving to next page after a sleep
    if num_inserts >= 5000:
        conn.commit()
        num_inserts = 0
    i += 1
    time.sleep(6)

# Close out
conn.commit()
cur.close()
conn.close()
print(f"Total time: {time.time() - start}s")
