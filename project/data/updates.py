from data_utils import pull_new_page_info, pull_updated_page_info, pull_updated_bills, pull_new_bills
from inserting_code import insert_bills
from datetime import date
import requests
import time
import psycopg2

conn = psycopg2.connect(
    database='billinois',
    host = os.environ['billinois-db-host'], 
    user= os.environ['billinois-db-user'],
    password=os.environ['billinois-db-password']
)
cur = conn.cursor()

today_date = date.today()
today_date = str(today_date)
# Inserting new bills, easy peasy
total_pages_new = pull_new_page_info(today_date)
num_new_inserts = 0
for i in range(1, total_pages_new+1):
    bills_from_page = pull_new_bills(i, today_date)
    if not bills_from_page:
        print("No new bills")
        break
    print(f"inserting new bills from page {i}")
    bills, sponsors, actions, inserts_on_page = insert_bills(bills_from_page)

    arguments_bills = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", bill).decode("utf-8") for bill in bills)
    arguments_sponsors = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s)", sponsor).decode("utf-8") for sponsor in sponsors)
    arguments_actions = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", action).decode("utf-8") for action in actions)

    cur.execute("INSERT INTO bills_table (bill_id, number, title, summary, status) VALUES " + arguments_bills)
    cur.execute("INSERT INTO sponsors_table (id, bill_id, sponsor_id, sponsor_name, party, position) VALUES " + arguments_sponsors)
    cur.execute("INSERT INTO actions_table (action_id, bill_id, description, date, category) VALUES " + arguments_actions)
    num_new_inserts += inserts_on_page
    if num_new_inserts >= 5000:
        conn.commit()
        num_new_inserts = 0
    i += 1
    time.sleep(6)
conn.commit()

# For updated bills, have to delete from DB first and reinsert
total_pages_updated = pull_updated_page_info(today_date)
num_updated_inserts = 0
for p in range(1, total_pages_updated+1):
    page_updated_bills = pull_updated_bills(p, today_date)
    if not page_updated_bills:
        print("No updates to bills")
        break
    print(f"deleting records from page {p}")
    for record in page_updated_bills:
        id_to_delete = record["id"]

        bill_delete_statement = """DELETE FROM bills_table WHERE bill_id = (%s)"""
        sponsors_delete_statement = """DELETE FROM sponsors_table WHERE bill_id = (%s)"""
        actions_delete_statement = """DELETE FROM actions_table WHERE bill_id = (%s)"""

        # Deleting from actions/sponsors first as PK issue
        cur.execute(actions_delete_statement, (id_to_delete,))
        cur.execute(sponsors_delete_statement, (id_to_delete,))
        cur.execute(bill_delete_statement, (id_to_delete,))

    print(f"inserting updated bills from page {p}")
    updated_bills, updated_sponsors, updated_actions, updated_inserts = insert_bills(page_updated_bills)
    arguments_bills_updated = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", bill).decode("utf-8") for bill in updated_bills)
    arguments_sponsors_updated = ','.join(cur.mogrify("(%s, %s, %s, %s, %s, %s)", sponsor).decode("utf-8") for sponsor in updated_sponsors)
    arguments_actions_updated = ','.join(cur.mogrify("(%s, %s, %s, %s, %s)", action).decode("utf-8") for action in updated_actions)

    cur.execute("INSERT INTO bills_table (bill_id, number, title, summary, status) VALUES " + arguments_bills_updated)
    cur.execute("INSERT INTO sponsors_table (id, bill_id, sponsor_id, sponsor_name, party, position) VALUES " + arguments_sponsors_updated)
    cur.execute("INSERT INTO actions_table (action_id, bill_id, description, date, category) VALUES " + arguments_actions_updated)

    num_updated_inserts += updated_inserts
    if num_updated_inserts >= 5000:
        conn.commit()
        num_updated_inserts = 0
    p+= 1
    time.sleep(6)
conn.commit()
cur.close()
conn.close()