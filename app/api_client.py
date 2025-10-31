import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import threading


class CountryLeadersAPI:
    """Handles all requests country and leader endpoints."""

    def __init__(self, root_url="https://country-leaders.onrender.com"):
        self.root_url = root_url
        self.cookie_url = "/cookie"
        self.countries_url = "/countries"
        self.leaders_url = "/leaders"
        # Thread-local sessions for thread safety
        self._thread_local = threading.local()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
        # I try to use higher pool_maxsize to optimize the performance of the API calls.
        adapter = HTTPAdapter(max_retries=retries, pool_connections=32, pool_maxsize=64)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _refresh_cookie(self, session: requests.Session) -> None:
        response = session.get(self.root_url + self.cookie_url)
        response.raise_for_status()
        print("Fetched/ refreshed cookie from server")

    def _get_thread_session(self) -> requests.Session:
        session = getattr(self._thread_local, "session", None)
        if session is None:
            session = self._create_session()
            self._refresh_cookie(session)
            self._thread_local.session = session
        return session

    def get_session(self) -> requests.Session:
        """Return a per-thread session with cookie set."""
        return self._get_thread_session()

    def get_countries(self) -> list:
        """Fetch list of all countries."""
        session = self._get_thread_session()
        try:
            r = session.get(self.root_url + self.countries_url)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            # If cookie-related issue, refresh and retry once
            if r is not None and r.status_code in (401, 403):
                self._refresh_cookie(session)
                r = session.get(self.root_url + self.countries_url)
                r.raise_for_status()
                return r.json()
            raise e

    def get_leaders_by_country(self, country: str) -> list:
        """Fetch all leaders for a specific country."""
        session = self._get_thread_session()
        try:
            r = session.get(self.root_url + self.leaders_url, params={"country": country})
            if r.status_code == 200:
                return r.json()
            if r.status_code in (401, 403):
                self._refresh_cookie(session)
                r = session.get(self.root_url + self.leaders_url, params={"country": country})
                if r.status_code == 200:
                    return r.json()
            print(f"Error: country {country}: {r.status_code}")
            return []
        except requests.RequestException as e:
            print(f"Request error for {country}: {e}")
            return []

    def get_leader_by_id(self, leader_id: str) -> dict:
        """Get a leader's details by ID."""
        session = self._get_thread_session()
        try:
            r = session.get(f"{self.root_url}/leader", params={"leader_id": leader_id})
            if r.status_code == 200:
                return r.json()
            if r.status_code in (401, 403):
                self._refresh_cookie(session)
                r = session.get(f"{self.root_url}/leader", params={"leader_id": leader_id})
                if r.status_code == 200:
                    return r.json()
            print(f"Error: leader_id{leader_id}: {r.status_code}")
            return {}
        except requests.RequestException as e:
            print(f"Request error for leader {leader_id}: {e}")
            return {}