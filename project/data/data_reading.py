"""
This file includes the code to ingestion all of the legislation from the 104th session
"""

import psycopg2
import os
import time
from data_utils import pull_page, insert_bills

start = time.time()

conn = psycopg2.connect(
    database="billinois",
    host=os.environ["billinois-db-host"],
    user=os.environ["billinois-db-user"],
    password=os.environ["billinois-db-password"],
)
cur = conn.cursor()

# Use helper function to get number of pages
max_pages = pull_page(1)["pagination"]

num_inserts = 0
for i in range(220, max_pages + 1):
    print(f"Pulling bills from page {i}")

    # Helper function runs query to get all bill info from current page
    page_info = pull_page(i)["results"]

    # Storing all info from one page in a list for mass insert
    bills, sponsors, actions, inserts_on_page, _ = insert_bills(page_info)
    num_inserts += inserts_on_page
    # Mass inserting with lists
    arguments_bills = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s)", bill).decode("utf-8") for bill in bills
    )
    arguments_sponsors = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s, %s)", sponsor).decode("utf-8") for sponsor in sponsors
    )
    arguments_actions = ",".join(
        cur.mogrify("(%s, %s, %s, %s, %s)", action).decode("utf-8") for action in actions
    )

    cur.execute(
        "INSERT INTO bills_table (bill_id, number, title, summary, status) VALUES "
        + arguments_bills
    )
    cur.execute(
        "INSERT INTO sponsors_table (id, bill_id, sponsor_id, sponsor_name, party, position) VALUES "
        + arguments_sponsors
    )
    cur.execute(
        "INSERT INTO actions_table (action_id, bill_id, description, date, category) VALUES "
        + arguments_actions
    )

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
