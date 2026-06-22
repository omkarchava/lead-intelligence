import os
import requests
from dotenv import load_dotenv

load_dotenv()

class SalesforceClient:

    def __init__(self):

        auth = requests.post(
            "https://orgfarm-3d56ab6832-dev-ed.develop.my.salesforce.com/services/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": os.getenv("SF_CLIENT_ID"),
                "client_secret": os.getenv("SF_CLIENT_SECRET")
            }
        ).json()

        self.token = auth["access_token"]
        self.instance = auth["instance_url"]

        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def query(self, soql):

        r = requests.get(
            f"{self.instance}/services/data/v64.0/query",
            headers=self.headers,
            params={"q": soql}
        )

        return r.json()

sf = SalesforceClient()