from api_client import CountryLeadersAPI
from wikipedia_scraper import WikipediaScraper
from leaders_manager import LeadersManager

def main():
    """Main execution function."""
    api = CountryLeadersAPI()
    scraper = WikipediaScraper()
    manager = LeadersManager(api, scraper)

    leaders = manager.get_all_leaders()

    print("\n" + "=" * 50)
    print("Adding Wikipedia paragraphs...")
    print("=" * 50)
    leaders = manager.add_wikipedia_paragraphs(leaders)

    print("\n" + "=" * 50)
    print("Saving results...")
    print("=" * 50)
    manager.save_to_json(leaders)

    print("\nProcess completed successfully!")


if __name__ == "__main__":
    main()