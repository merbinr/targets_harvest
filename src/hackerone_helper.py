import os
import sys
import requests
import time



class HackeroneHelper:
    def __init__(self, db_helper):
        self.base_url = "https://api.hackerone.com"
        self.username = os.getenv("HACKERONE_USERNAME")
        self.token = os.getenv("HACKERONE_TOKEN")
        self.headers = {
            'Accept': 'application/json'
            }
        self.db_helper = db_helper
        self.__check_envs()
    
    def __check_envs(self):
        if not os.getenv("HACKERONE_USERNAME"):
            print("HACKERONE_USERNAME is not set")
            sys.exit(1)
        if not os.getenv("HACKERONE_TOKEN"):
            print("HACKERONE_TOKEN is not set")
            sys.exit(1)
    
    def get_scopes_list(self, program_handle):
        next_url = None
        while True:
            if next_url:
                url = next_url
            else:
                url = f"{self.base_url}/v1/hackers/programs/{program_handle}/structured_scopes?page[size]=100&page[number]=1"

            print(f"Fetching data from {url}")
            res = requests.get(url=url, auth=(self.username, self.token), headers=self.headers)

            if res.status_code == 429:
                print("Rate limit exceeded")
                time.sleep(60)
                continue

            if res.status_code == 200:
                scopes_data = res.json()
                for each_scope_data in scopes_data.get("data"):
                    data = {
                        "platform": "hackerone",
                        "program_id": program_handle,
                        "asset": each_scope_data.get("attributes").get("asset_identifier"),
                        "asset_type": each_scope_data.get("attributes").get("asset_type"),
                        "eligible_for_bounty": each_scope_data.get("attributes").get("eligible_for_bounty"),
                        "eligible_for_submission": each_scope_data.get("attributes").get("eligible_for_submission"),
                        "max_severity": each_scope_data.get("attributes").get("max_severity"),
                        "created_at": each_scope_data.get("attributes").get("created_at"),
                        "updated_at": each_scope_data.get("attributes").get("updated_at")
                    }
                    self.db_helper.insert_scope(data)
                if scopes_data.get("links").get("next"):
                    print(f"Next url: {scopes_data.get('links').get('next')}")
                    next_url = scopes_data.get("links").get("next")
                else:
                    print("No more data to fetch, breaking the loop\n")
                    return
            else:
                print(f"Error on url {url}, status_code: {res.status_code}")
                sys.exit(1)
            
    
    def get_programes_list(self):
        next_url = None
        while True:
            if next_url:
                url = next_url
            else:
                url = f"{self.base_url}/v1/hackers/programs?page[size]=100&page[number]=1"

            print(f"Fetching data from {url}")
            res = requests.get(url=url, auth=(self.username, self.token), headers=self.headers)

            if res.status_code == 429:
                print("Rate limit exceeded")
                time.sleep(60)
                continue

            if res.status_code == 200:
                programs_data = res.json()
                for each_program_data in programs_data.get("data"):
                    program_handle = each_program_data.get("attributes").get("handle")
                    data = {
                        "platform": "hackerone",
                        "program_id": program_handle,
                        "name": each_program_data.get("attributes").get("name"),
                        "currency": each_program_data.get("attributes").get("currency"),
                        "state": each_program_data.get("attributes").get("submission_state"),
                        "triage_active": each_program_data.get("attributes").get("triage_active"),
                        "visibility": each_program_data.get("attributes").get("state"),
                        "created_at": each_program_data.get("attributes").get("started_accepting_at"),
                        "offers_bounties": each_program_data.get("attributes").get("offers_bounties")
                    }
                    self.db_helper.insert_program(data)
                    self.get_scopes_list(program_handle=program_handle)
                if programs_data.get("links").get("next"):
                    print(f"Next url: {programs_data.get('links').get('next')}")
                    next_url = programs_data.get("links").get("next")
                else:
                    print("No more data to fetch, breaking the loop\n")
                    return   
            else:
                print(f"Error on url {url}, status_code: {res.status_code}")
                sys.exit(1)
        
    

