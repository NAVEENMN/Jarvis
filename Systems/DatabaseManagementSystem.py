import os
import json
import requests
from datetime import date


class DatabaseManagementSystem:
    def __init__(self):
        self.url = "https://data.mongodb-api.com/app/data-xduww/endpoint/data/v1"
        self.database_name = None
        self.cluster_name = 'PersonalCluster-0'
        self.header = {
            'Content-Type': 'application/json',
            'Access-Control-Request-Headers': '*',
            'api-key': os.environ.get('DBKEY')
        }

    def change_database(self, db_name):
        self.database_name = db_name

    def add_a_record(self, collection, key="date", value=str(date.today()), content=None):
        print(f"*** INFO: Adding a record {self.database_name}:{collection}:{key}")
        payload = json.dumps({
            "collection": collection,
            "database": self.database_name,
            "dataSource": self.cluster_name,
            "document": {key: value, 'data': content}
        })
        response = requests.request("POST",
                                    f'{self.url}/action/insertOne',
                                    headers=self.header,
                                    data=payload)
        if response.status_code != 201:
            print(f"*** ERROR: Adding a record {key}: {response}")
            return False
        print(f"*** INFO: Successfully added a record {key}")
        return True

    def delete_a_record(self, collection, key="date", value=str(date.today())):
        print(f'*** WARNING: Deleting a record {self.database_name}:{collection}:{key}')
        payload = json.dumps({
            "collection": collection,
            "database": self.database_name,
            "dataSource": "PersonalCluster-0",
            "filter": {key: value}
        })
        response = requests.request("POST",
                                    f'{self.url}/action/deleteOne',
                                    headers=self.header,
                                    data=payload)

        if response.status_code != 200:
            print(f"*** ERROR : Failed to delete record: {key}")
            return False
        print(f"*** INFO : Successfully deleted a record {key}")
        return True

    def get_a_record(self, collection, key="date", value=str(date.today())):
        print(f"*** INFO: Getting a record{ self.database_name}:{collection}:{key}")
        payload = json.dumps({
            "collection": collection,
            "database": self.database_name,
            "dataSource": "PersonalCluster-0",
            "filter": {key: value}
        })
        url = f'{self.url}/action/findOne'
        response = requests.request("POST",
                                    url,
                                    headers=self.header,
                                    data=payload)
        if response.status_code != 200:
            print(f"*** INFO: Failed to retrieve data: {response.status_code}")
            return None, False

        if not response.json()['document']:
            print(f"*** INFO: No such record found")
            return None, False

        return response.json(), True