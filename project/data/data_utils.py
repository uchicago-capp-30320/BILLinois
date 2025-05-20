import os
import requests
from topics.topics_classifier import get_topics_from_bill
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(
    DEBUG=(bool, False),
)
env.read_env(BASE_DIR / ".env")

API_KEY = os.getenv("OPENSTATES_KEY")
base_url = "https://v3.openstates.org/bills?"
vars_to_include = ["sponsorships", "abstracts", "actions"]
per_page_val = 20  # Highest it can go


# Single function for all API calls
def pull_page(state: str, session: str, page_num: int, date=None):
    """
    Single function for performing either all bills or bills with actions
    since a given date. If page number is not specified, the first page is returned.
    If date is not specified, all bills for the provided state/session are returned.

    Returns the raw JSON response, which includes two dictionaries:
        ['pagination']: includes metadata on the number of total pages returned
        ['results']: the bill data for the given page
    """
    params = {
        "apikey": API_KEY,
        "jurisdiction": state,
        "include": vars_to_include,
        "session": session,
        "per_page": per_page_val,
        "page": page_num,
    }
    if date:
        params["action_since"] = date
    response = requests.get(base_url, params)

    raw_results_json = response.json()
    results = raw_results_json["results"]
    max_pages = raw_results_json["pagination"]["max_page"]
    return results, max_pages


def insert_bills(series_of_bills: dict):
    """
    This function creates the lists of bills, sponsors, actions, and updates
    needed for mass insertion into the tables

    Args:
        series_of_bills (json): A JSON object from the Openstates API with all
        the bills on a given page

    Returns:
        page_bills (list[list]): A list of lists, where each list includes information
                                on a bill's ID, number, title, summary, and status
        page_sponsors (list[list]): A list of lists, where each list includes information
                                    for a given sponsor on a given bill.
        page_actions (list[list]): A list of lists, where each list includes information
                                    for a given action on a given bill.
        page_insert (int): The number of total inserts across all tables for this
                            page (used to time transactions)
        page_updates (list[list]): A list of lists, where each list includes
                                information on a bill that users need to be
                                notified about (ONLY returned when analyzing newly updated bills)
    """
    page_inserts = 0
    page_bills = []
    page_sponsors = []
    page_actions = []
    page_updates = []
    page_topics = []

    for record in series_of_bills:
        # Bill
        bill_id_val = record["id"]
        number_val = record["identifier"]
        title_val = record["title"]
        summary_val = record["abstracts"][0]["abstract"]
        status_val = record["latest_action_description"]
        state_val = record["jurisdiction"]["name"]
        session_val = record["session"]

        page_bills.append(
            [bill_id_val, number_val, title_val, summary_val, status_val, state_val, session_val]
        )
        page_inserts += 1

        # Topics within a bill
        assigned_topics = get_topics_from_bill(title_val, summary_val)
        if assigned_topics:
            for topic in assigned_topics:
                page_topics.append([bill_id_val, topic])

        # Sponsors
        sponsors_list = record["sponsorships"]
        for s in sponsors_list:
            # Handling sponsors without recognized "IDs" in OpenStates
            sponsorship_id = s["id"]
            try:
                sponsor_id_val = s["person"]["id"]
                sponsor_name_val = s["person"]["name"]
                sponsor_party_val = s["person"]["party"]
                sponsor_position_val = s["person"]["current_role"]["title"]
            except KeyError:
                sponsor_id_val = None
                sponsor_name_val = s["name"]
                sponsor_party_val = None
                sponsor_position_val = None

            page_sponsors.append(
                [
                    sponsorship_id,
                    bill_id_val,
                    sponsor_id_val,
                    sponsor_name_val,
                    sponsor_party_val,
                    sponsor_position_val,
                ]
            )
            page_inserts += 1

        # Actions
        actions_list = record["actions"]
        something_to_update = False
        for a in actions_list:
            action_id = a["id"]
            description_val = a["description"]
            date_val = a["date"]
            chamber_val = a["organization"]["name"]
            # Adding action classification for the actions that have it
            if a["classification"]:
                classification_val = a["classification"][0]  # Taking first classification
                # If an action is 'significant' (non-null classification), check
                # if its date is the latest date. If so, users should be updated.
                # NOTE: This var iteratively replaced until we have latest update
                if date_val == record["latest_action_date"]:
                    something_to_update = True
                    most_recent_significant = [
                        bill_id_val,
                        classification_val,
                        description_val,
                        chamber_val,
                        action_id,
                        date_val,
                    ]
            else:
                classification_val = None

            page_actions.append(
                [action_id, bill_id_val, description_val, chamber_val, date_val, classification_val]
            )
            page_inserts += 1
        # For the most RECENT significant action, create entry in updates table
        if something_to_update:
            page_updates.append(most_recent_significant)

    return {
        "bills_from_page": page_bills,
        "sponsors_from_page": page_sponsors,
        "actions_from_page": page_actions,
        "inserts_from_page": page_inserts,
        "updates_from_page": page_updates,
        "topics_from_page": page_topics,
    }
