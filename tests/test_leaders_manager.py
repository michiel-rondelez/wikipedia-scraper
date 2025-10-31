from app.leaders_manager import LeadersManager


class DummyAPI:
    def __init__(self, countries, leaders_by_country):
        self._countries = countries
        self._leaders_by_country = leaders_by_country

    def get_countries(self):
        return list(self._countries)

    def get_leaders_by_country(self, country):
        return list(self._leaders_by_country.get(country, []))

    def get_session(self):
        # Not used in these tests after refactor
        raise RuntimeError("should not be called")


class DummyScraper:
    def get_first_paragraph(self, url, first_name, session):
        return f"{first_name} - paragraph"


def test_get_all_leaders_concurrent_aggregates_by_country():
    api = DummyAPI(countries=["A", "B"], leaders_by_country={
        "A": [{"first_name": "John", "wikipedia_url": "u1"}],
        "B": [{"first_name": "Jane", "wikipedia_url": "u2"}],
    })
    manager = LeadersManager(api, DummyScraper(), max_workers=2)

    data = manager.get_all_leaders()
    assert set(data.keys()) == {"A", "B"}
    assert data["A"][0]["first_name"] == "John"
    assert data["B"][0]["first_name"] == "Jane"


def test_add_wikipedia_paragraphs_preserves_order_and_sets_text():
    api = DummyAPI(countries=[], leaders_by_country={})
    manager = LeadersManager(api, DummyScraper(), max_workers=3)
    leaders_by_country = {
        "A": [
            {"first_name": "Zed", "wikipedia_url": "u1"},
            {"first_name": "Ann", "wikipedia_url": "u2"},
            {"first_name": "Bob", "wikipedia_url": "u3"},
        ]
    }

    result = manager.add_wikipedia_paragraphs(leaders_by_country)
    names = [l["first_name"] for l in result["A"]]
    assert names == ["Zed", "Ann", "Bob"]
    assert all(l["paragraph"].endswith("- paragraph") for l in result["A"])

