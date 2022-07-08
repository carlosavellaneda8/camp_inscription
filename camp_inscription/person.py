"""Retrieve a person's data for the camp register"""
import requests
import pandas as pd
from camp_inscription.settings import API_KEY, APP_KEY, PAYMENT_TABLE, TEAM_TABLE, SUPPORT_TABLE

base_url = "https://api.airtable.com/v0/{app_key}/{table}"
filter_option = "?filterByFormula=%7BN%C3%BAmero+de+documento%7D%3D{id_number}"
headers = {"Authorization": f"Bearer {API_KEY}"}


def format_url(id_number: int, table: str) -> str:
    """Format the base url to query the data"""
    final_url = base_url.format(app_key=APP_KEY, table=table)
    final_url = final_url + filter_option.format(id_number=id_number)
    return final_url


class AllPersons:

    """Class that retrieves all ids"""

    def __init__(self):
        self.url = base_url.format(app_key=APP_KEY, table=PAYMENT_TABLE) + "?fields%5B%5D=N%C3%BAmero+de+documento"

    def get_ids(self):
        params = ()
        records = []
        run = True
        while run:
            r = requests.get(self.url, params=params, headers=headers)
            data = pd.json_normalize(r.json()["records"])
            records.append(data)
            if "offset" in r.json():
                run = True
                params = (("offset", r.json()["offset"]), )
            else:
                run = False
        output_data = pd.concat(records)
        return output_data["fields.Número de documento"].drop_duplicates().tolist()

class Person:

    """Class that contains the main info for a person's inscription to the camp"""

    def __init__(self, id_number: int):
        self.id_number = id_number

    def get_support_data(self) -> pd.DataFrame:
        """Get the data if the person is supported by the Church"""
        return self._get_table_data(table=SUPPORT_TABLE)

    def get_team_data(self) -> pd.DataFrame:
        """Get the data of the person's camp team"""
        return self._get_table_data(table=TEAM_TABLE)

    def get_payment_data(self) -> pd.DataFrame:
        """Get the data of the person's payment"""
        return self._get_table_data(table=PAYMENT_TABLE)

    def _get_table_data(self, table: str) -> pd.DataFrame:
        url = format_url(id_number=self.id_number, table=table)
        return self._get_url_data(url)

    @staticmethod
    def _get_url_data(url: str) -> pd.DataFrame:
        """Get data from Airtable's API based on a url"""
        r = requests.get(url, headers=headers)
        data = r.json()
        return pd.json_normalize(data["records"])
