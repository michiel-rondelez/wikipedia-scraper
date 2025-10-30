import requests
import time


class CountryLeadersAPI:
    """Handles all requests country and leader endpoints."""

    def __init__(self, root_url="https://country-leaders.onrender.com"):
        self.root_url = root_url
        self.cookie_url = "/cookie"
        self.countries_url = "/countries"
        self.leaders_url = "/leaders"

    def get_session(self) -> requests.Session:
        """Always get a new session cookie from the server."""
        session = requests.Session()
        response = session.get(self.root_url + self.cookie_url)
        response.raise_for_status()
        print("Fetched new cookie from server")
        return session

    def get_countries(self) -> list:
        """Fetch list of all countries."""
        session = self.get_session()
        r = session.get(self.root_url + self.countries_url)
        r.raise_for_status()
        return r.json()

    def get_leaders_by_country(self, country: str) -> list:
        """Fetch all leaders for a specific country."""
        session = self.get_session()
        r = session.get(self.root_url + self.leaders_url, params={"country": country})
        if r.status_code == 200:
            return r.json()
        print(f"Error: country {country}: {r.status_code}")
        return []

    def get_leader_by_id(self, leader_id: str) -> dict:
        """Get a leader's details by ID."""
        session = self.get_session()
        r = session.get(f"{self.root_url}/leader", params={"leader_id": leader_id})
        if r.status_code == 200:
            return r.json()
        print(f"Error: leader_id{leader_id}: {r.status_code}")
        return {}