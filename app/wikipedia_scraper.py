import re
import requests
from bs4 import BeautifulSoup


class WikipediaScraper:
    """Handles fetching and cleaning Wikipedia paragraphs."""

    def __init__(self):
        self.headers = {"User-Agent": "MyPythonApp/1.0 (contact: michiel.rondelez1@gmail.com)"}

    def clean_text(self, text: str) -> str:
        """Remove footnote markers, extra spaces, and special symbols."""
        text = re.sub(r'\[\d+\]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[\u2190-\u21FF\u2300-\u23FF\u2460-\u24FF\u2500-\u257F\u2600-\u26FF\u2700-\u27BF\U0001F300-\U0001FAFF]', '', text)
        return text.strip()

    def get_first_paragraph(self, url: str, first_name: str, session: requests.Session) -> str:
        """Fetch the first relevant paragraph from Wikipedia."""
        r = session.get(url, headers=self.headers)
        if r.status_code == 403:
            print(f"Error - Forbidden: {url}")
            return ""
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        

        for p_tag in soup.find_all("p"):
            if "mw-empty-elt" in p_tag.get("class", []):
                continue
            for b in p_tag.find_all("b"):
                if first_name.lower() in b.get_text(" ", strip=True).lower():
                    text = self.clean_text(p_tag.get_text(" ", strip=True))
                    print(f"Found paragraph for {first_name}: {text[:100]}...")
                    return text

        p_tag = soup.select_one("p:not(.mw-empty-elt)")
        if not p_tag:
            print(f"No paragraph found: {url}")
            return ""

        text = self.clean_text(p_tag.get_text(" ", strip=True))
        print(f"Using fallback paragraph for {first_name}: {text[:100]}...")
        return text