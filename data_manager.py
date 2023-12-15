from config import SHEETY_BEARER_TOKEN, SHEETY_USER_ID_KEY
import requests
from pprint import pprint

# This class is responsible for talking to the Google Sheet.
class DataManager:
    def __init__(self) -> None:
        self.headers = {"Authorization": f"Bearer {SHEETY_BEARER_TOKEN}"}
        self.user_id_key = SHEETY_USER_ID_KEY
        self.data = []

    def getData(self):
        response = requests.get(
            f"https://api.sheety.co/{self.user_id_key}/flightSearch/sheet1",
            headers=self.headers,
        ).json()
        print(response)
        sheet_data = response["sheet1"]
        self.data = sheet_data
        return sheet_data

    def updateData(self, newData):
        self.data = newData
        for entry in self.data:
            updates = {"sheet1": {"iataCode": entry["iataCode"]}}
            response = requests.put(
                f"https://api.sheety.co/{self.user_id_key}/flightSearch/sheet1/{entry['id']}", json=updates, headers=self.headers)
            print(response.text)
