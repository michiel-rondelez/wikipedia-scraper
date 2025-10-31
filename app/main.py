from api_client import CountryLeadersAPI
from wikipedia_scraper import WikipediaScraper
from leaders_manager import LeadersManager
import time

def main():
    """Main execution function."""
    api = CountryLeadersAPI()
    scraper = WikipediaScraper()
    manager = LeadersManager(api, scraper)

    #start timer
    start_time_leaders = time.time()

    leaders = manager.get_all_leaders()

    #end timer
    end_time_leaders = time.time()


    print("\n" + "=" * 50)
    print("Adding Wikipedia paragraphs...")
    print("=" * 50)

    #start timer
    start_time = time.time()
    leaders = manager.add_wikipedia_paragraphs(leaders)

    #end timer
    end_time = time.time()

    print("\n" + "=" * 50)
    print("Saving results...")
    print("=" * 50)
    manager.save_to_json(leaders)
    manager.save_to_csv(leaders)
    print("\nProcess completed successfully!")
    print("=" * 50)
    print(f"Time taken to get all leaders: {end_time_leaders - start_time_leaders} seconds")
    print(f"Time taken to add Wikipedia paragraphs: {end_time - start_time} seconds")
    print(f"Total time taken: {end_time - start_time_leaders} seconds")
    print("=" * 50)

if __name__ == "__main__":
    main()