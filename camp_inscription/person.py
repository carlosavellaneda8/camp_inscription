"""Retrieve a person's data for the camp register"""
import requests
from camp_inscription.settings import API_KEY, APP_KEY, TEAM_TABLE, META_TABLE

BASE_URL = "https://api.airtable.com/v0/{app_key}/{table}"
headers = {"Authorization": f"Bearer {API_KEY}"}


class AllPersons:

    """Class that retrieves all ids"""

    def __init__(self):
        self.teams_url = BASE_URL.format(app_key=APP_KEY, table=TEAM_TABLE)
        self.meta_url = BASE_URL.format(app_key=APP_KEY, table=META_TABLE)
        self.records = []
        self.meta = []

    def get_teams_data(self) -> None:
        """Updates the records from all people"""
        self.records += self._get_data(url=self.teams_url)

    def get_meta_data(self) -> None:
        """Updates the metadata of all teams"""
        self.meta += self._get_data(url=self.meta_url)

    @staticmethod
    def _get_data(url: str) -> list:
        """Retrieve in a list all data from a specified url"""
        params = ()
        records = []
        run = True
        counter = 0
        while run:
            counter += 1
            r = requests.get(url, params=params, headers=headers)
            data = r.json()["records"]
            records.extend(data)
            if "offset" in r.json():
                run = True
                params = (("offset", r.json()["offset"]), )
            else:
                run = False
        print(f"API total requests: {counter}")
        return records


class Person:

    """Class that retrieves the main attributes of a person based on its id number"""

    def __init__(self, id_number: int):
        self.id_number = id_number
        self.name = None
        self.team = None
        self.team_info = {}

    def get_person_info(self, records: list) -> None:
        """Retrieves the person's name and team"""
        data = [
            record["fields"] for record in records
            if record["fields"]["Número de documento"] == self.id_number
        ][0]
        self.name = data["nombre"].title()
        self.team = data["distrito"]

    def get_team_info(self, meta: list) -> None:
        """Retrieve the team's meta-data"""
        assert self.team is not None
        data = [
            record["fields"] for record in meta if record["fields"]["distrito"] == self.team
        ][0]
        self.team_info.update(data)
