def insert_bills(series_of_bills):
    page_inserts = 0
    page_bills = []
    page_sponsors = []
    page_actions = []
        
    for record in series_of_bills:
    # Bill
        bill_id_val = record["id"]
        number_val = record["identifier"]
        title_val = record["title"]
        summary_val = record["abstracts"][0]["abstract"]
        status_val = record["latest_action_description"]

        page_bills.append([bill_id_val, number_val, title_val, summary_val, status_val])
        page_inserts +=1

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
            
            page_sponsors.append([sponsorship_id, bill_id_val, sponsor_id_val, sponsor_name_val, sponsor_party_val, sponsor_position_val])
            page_inserts += 1

        # Actions
        actions_list = record["actions"]
        for a in actions_list:
            action_id = a["id"]
            description_val = a["description"]
            date_val = a["date"]
            # Adding action classification for the actions that have it
            if a["classification"]:
                classification_val = a["classification"][0] # Taking first classification
            else:
                classification_val = None
            
            page_actions.append([action_id, bill_id_val, description_val, date_val, classification_val])
            page_inserts +=1

    return page_bills, page_sponsors, page_actions, page_inserts 