import os
import requests

API_KEY = os.environ["openstates_key"]
base_url = "https://v3.openstates.org/bills?"
vars_to_include = ["sponsorships", "abstracts", "actions"]


def pull_bills():
    response = requests.get(
        base_url, {"apikey": API_KEY, "jurisdiction": "IL", "include": vars_to_include}
    )

    return response.json()


def parse_bills():
    response_raw = pull_bills()
    results = response_raw["results"]  # NOTE: Only grabbing 1st page for now
    return results
