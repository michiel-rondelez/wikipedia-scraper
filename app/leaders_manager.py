import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from api_client import CountryLeadersAPI
from wikipedia_scraper import WikipediaScraper


class LeadersManager:
    """Fetching leaders and adding wikipedia paragraphs."""

    def __init__(self, api: CountryLeadersAPI, scraper: WikipediaScraper, max_workers: int = 6):
        self.api = api
        self.scraper = scraper
        self.max_workers = max_workers

    def get_all_leaders(self) -> dict:
        """Fetch leaders per country concurrently."""
        countries = self.api.get_countries()
        data = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            future_to_country = {
                pool.submit(self.api.get_leaders_by_country, country): country
                for country in countries
            }
            for future in as_completed(future_to_country):
                country = future_to_country[future]
                print(f"Fetching leaders for {country}...")
                try:
                    data[country] = future.result()
                except Exception:
                    data[country] = []

        return data

    def add_wikipedia_paragraphs(self, leaders_by_country: dict):
        """Add Wikipedia paragraph for each leader concurrently per country."""
        # Build a small pool of sessions with connection pooling
        retries = Retry(total=3, backoff_factor=0.2, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries, pool_connections=self.max_workers * 2, pool_maxsize=self.max_workers * 2)
        wiki_sessions = []
        for _ in range(self.max_workers):
            s = requests.Session()
            s.headers.update({"User-Agent": "MyPythonApp/1.0 (contact: michiel.rondelez1@gmail.com)"})
            s.mount("http://", adapter)
            s.mount("https://", adapter)
            wiki_sessions.append(s)

        def enrich_leader(leader: dict, session: requests.Session) -> dict:
            url = leader.get("wikipedia_url")
            first_name = leader.get("first_name", "")
            if not url:
                leader["paragraph"] = ""
                return leader
            try:
                leader["paragraph"] = self.scraper.get_first_paragraph(url, first_name, session)
            except Exception:
                leader["paragraph"] = ""
            return leader

        for country, leaders in leaders_by_country.items():
            print(f"Processing {country}...")
            # Preserve original order
            indexed = list(enumerate(leaders))
            results = [None] * len(indexed)
            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                # simple round-robin assignment of prebuilt sessions
                future_to_index = {
                    pool.submit(enrich_leader, leader, wiki_sessions[idx % len(wiki_sessions)]): idx
                    for idx, leader in indexed
                }
                for future in as_completed(future_to_index):
                    idx = future_to_index[future]
                    try:
                        results[idx] = future.result()
                    except Exception:
                        # Fallback to empty paragraph if task failed
                        failed = dict(leaders[idx])
                        failed["paragraph"] = ""
                        results[idx] = failed
            leaders_by_country[country] = results

        return leaders_by_country

    def save_to_json(self, data: dict, filename="leaders_with_paragraphs.json"):
        """Save data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {filename}")