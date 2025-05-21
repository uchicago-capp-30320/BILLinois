import psycopg2
import os
from samples_helpers import parse_bills

# Gathering bills, connecting to DB
bill_info = parse_bills()
conn = psycopg2.connect(
    database="billinois",
    host=os.environ["course_db_host"],
    user=os.environ["course_db_user"],
    password=os.environ["course_db_password"],
)

# Connecting to cursor, creating tables
cur = conn.cursor()

# When doing on lots of records, start transaction here
for record in bill_info:
    id_val = record["id"]
    number_val = record["identifier"]
    title_val = record["title"]
    summary_val = record["abstracts"][0]["abstract"]
    status_val = record["latest_action_description"]

    # Inserting into bills
    insert_statement = """
    INSERT INTO bills_mock (bill_id, number, title, summary, status) VALUES (%s, %s, %s, %s, %s)
    """
    cur.execute(insert_statement, (id_val, number_val, title_val, summary_val, status_val))

    # Leaving topics blank for now -- haven't decided method of topic determination

    # Sponsors
    sponsors_list = record["sponsorships"]
    for s in sponsors_list:
        # Only keep sponsors who are a known person to OpenStates
        try:
            sponsorship_id = s["id"]
            sponsor_id_val = s["person"]["id"]
            sponsor_name_val = s["person"]["name"]
        except Exception as e:
            print(f"Error with sponsor data: {e}")
            continue
        insert_sponsor_statement = """
        INSERT INTO sponsors_mock (id, bill_id, sponsor_id, sponsor_name) VALUES (%s, %s, %s, %s)
        """
        # Using bill id from outer loop
        cur.execute(
            insert_sponsor_statement, (sponsorship_id, id_val, sponsor_id_val, sponsor_name_val)
        )

    # Actions
    actions_list = record["actions"]
    for a in actions_list:
        action_id = a["id"]
        description_val = a["description"]
        date_val = a["date"]
        insert_action_statement = """
        INSERT INTO actions_mock (bill_id, action_id, description, date) VALUES (%s, %s, %s, %s)
        """
        # Using bill id from outer loop
        cur.execute(insert_action_statement, (id_val, action_id, description_val, date_val))

# Close out
conn.commit()
cur.close()
conn.close()
