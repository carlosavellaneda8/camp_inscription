"""Retrieve a person's data for the camp register"""
import requests
import pandas as pd
from camp_inscription.settings import API_KEY, APP_KEY, PAYMENT_TABLE, TEAM_TABLE

base_url = "https://api.airtable.com/v0/{app_key}/{table}"
filter_option = "?filterByFormula=%7BN%C3%BAmero+de+documento%7D%3D{id_number}"
headers = {"Authorization": f"Bearer {API_KEY}"}


def format_url(id_number: int, table: str) -> str:
    """Format the base url to query the data"""
    final_url = base_url.format(app_key=APP_KEY, table=table)
    final_url = final_url + filter_option.format(id_number=id_number)
    return final_url


class Person:

    """Class that contains the main info for a person's inscription to the camp"""

    def __init__(self, id: int):
        self.id = id

    def get_support_data(self):
        """Get the data if the person is supported by the Church"""
        pass

    def get_team_data(self):
        """Get the data of the person's camp team"""
        url = format_url(id_number=self.id, table=TEAM_TABLE)
        return self._get_url_data(url)

    def get_payment_data(self):
        """Get the data of the person's payment"""
        url = format_url(id_number=self.id, table=PAYMENT_TABLE)
        return self._get_url_data(url)

    @staticmethod
    def _get_url_data(url: str) -> pd.DataFrame:
        """Get data from Airtable's API based on a url"""
        r = requests.get(url, headers=headers)
        data = r.json()
        return pd.json_normalize(data["records"])
