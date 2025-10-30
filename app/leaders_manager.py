import json
from api_client import CountryLeadersAPI
from wikipedia_scraper import WikipediaScraper


class LeadersManager:
    """Fetching leaders and adding wikipedia paragraphs."""

    def __init__(self, api: CountryLeadersAPI, scraper: WikipediaScraper):
        self.api = api
        self.scraper = scraper

    def get_all_leaders(self) -> dict:
        """Fetch leaders per country and ensure last_name completeness."""
        countries = self.api.get_countries()
        data = {}

        for country in countries:
            leaders_from_country = self.api.get_leaders_by_country(country)
            print(f"Fetching leaders for {country}...")
            data[country] = leaders_from_country

        return data

    def add_wikipedia_paragraphs(self, leaders_by_country: dict):
        """Add Wikipedia paragraph for each leader."""
        session = self.api.get_session()
        for country, leaders in leaders_by_country.items():
            print(f"Processing {country}...")
            for leader in leaders:
                url = leader.get("wikipedia_url")
                first_name = leader.get("first_name", "")
                leader["paragraph"] = (
                    self.scraper.get_first_paragraph(url, first_name, session)
                    if url else ""
                )
        return leaders_by_country

    def save_to_json(self, data: dict, filename="leaders_with_paragraphs.json"):
        """Save data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Saved to {filename}")