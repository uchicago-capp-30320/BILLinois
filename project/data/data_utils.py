import os
import requests

API_KEY = os.environ["openstates_key"]
base_url = "https://v3.openstates.org/bills?"
vars_to_include = ['sponsorships', 'abstracts', 'actions']
per_page_val = 20 # Highest it can go

# echo experiment i feel like im going insane
def master_pull_page(type_of_pull:str, page_num:int, date=None):
    """
    type_of_pull (str): either "all", "new", or "updated". Dictates if we're
    pulling all bills in a session, newly created bills since a given date, 
    or updated bills since the given date. 
    """
    query_args = {'apikey': API_KEY,
                        'jurisdiction': "IL",
                        'include': vars_to_include, 
                        'session': "104th", 
                        'per_page': per_page_val, 
                        'page': page_num}
    if type_of_pull == "new":
        query_args["created_since"] = date
    if type_of_pull == "updated":
        query_args["updated_since"] = date
    response = requests.get(base_url, query_args)
    raw_bills_json = response.json()
    bills = raw_bills_json['results']
    return bills


# Old method
def pull_page(page_num, date=None):
    response = requests.get(base_url, {'apikey': API_KEY,
                                       'jurisdiction': "IL",
                                       'include': vars_to_include, 
                                       'session': "104th", 
                                       'per_page': per_page_val, 
                                       'page': page_num})
    
    raw_bills_json = response.json()
    raw_bills = raw_bills_json['results']
    return raw_bills

def pull_new_bills(page_num, date):
    response = requests.get(base_url, {'apikey': API_KEY,
                                       'jurisdiction': "IL",
                                       'include': vars_to_include, 
                                       'session': "104th", 
                                       'per_page': per_page_val, 
                                       'page': page_num, 
                                       'created_since': date})
    
    new_bills_json = response.json()
    new_bills = new_bills_json['results']
    return new_bills

def pull_updated_bills(page_num, date):
    response = requests.get(base_url, {'apikey': API_KEY,
                                       'jurisdiction': "IL",
                                       'include': vars_to_include, 
                                       'session': "104th", 
                                       'per_page': per_page_val, 
                                       'page': page_num, 
                                       'updated_since': date})
    
    updated_bills_json = response.json()
    updated_bills = updated_bills_json['results']
    return updated_bills

def get_page_info():
    response = requests.get(base_url, {'apikey': API_KEY,
                                       'jurisdiction': "IL",
                                       'include': vars_to_include, 
                                       'session': "104th", 
                                       'per_page': per_page_val})
    raw_pagination = response.json()['pagination']
    total_pages = raw_pagination['max_page']
    return total_pages

def pull_new_page_info(date):
    response = requests.get(base_url, {'apikey': API_KEY,
                                    'jurisdiction': "IL",
                                    'include': vars_to_include, 
                                    'session': "104th", 
                                    'per_page': per_page_val, 
                                    'created_since': date})
    raw_pagination = response.json()['pagination']
    total_pages = raw_pagination['max_page']
    return total_pages

def pull_updated_page_info(date):
    response = requests.get(base_url, {'apikey': API_KEY,
                                    'jurisdiction': "IL",
                                    'include': vars_to_include, 
                                    'session': "104th", 
                                    'per_page': per_page_val, 
                                    'updated_since': date})
    raw_pagination = response.json()['pagination']
    total_pages = raw_pagination['max_page']
    return total_pages

