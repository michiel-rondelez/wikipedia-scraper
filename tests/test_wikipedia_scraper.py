import types
from app.wikipedia_scraper import WikipediaScraper


class FakeResponse:
    def __init__(self, status_code: int, text: str = ""):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if 400 <= self.status_code:
            raise Exception(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, response: FakeResponse):
        self._response = response

    def get(self, url, headers=None):
        return self._response


def test_clean_text_removes_footnotes_and_symbols():
    scraper = WikipediaScraper()
    raw = "John Doe [1] was born in 1970. → ← ★"
    cleaned = scraper.clean_text(raw)
    assert "[1]" not in cleaned
    assert "→" not in cleaned and "←" not in cleaned and "★" not in cleaned
    assert "  " not in cleaned


def test_get_first_paragraph_prefers_bold_with_first_name():
    html = """
    <html><body>
      <p class="mw-empty-elt"></p>
      <p><b>John</b> is a leader. Second sentence.</p>
      <p>Another paragraph.</p>
    </body></html>
    """
    scraper = WikipediaScraper()
    session = FakeSession(FakeResponse(200, html))
    paragraph = scraper.get_first_paragraph("http://example.com", "John", session)
    assert paragraph.startswith("John is a leader.")


def test_get_first_paragraph_uses_fallback_when_no_bold_match():
    html = """
    <html><body>
      <p>First para without bold.</p>
      <p>Second para.</p>
    </body></html>
    """
    scraper = WikipediaScraper()
    session = FakeSession(FakeResponse(200, html))
    paragraph = scraper.get_first_paragraph("http://example.com", "NonExisting", session)
    assert paragraph == "First para without bold."

