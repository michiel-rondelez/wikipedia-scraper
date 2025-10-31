import threading
from types import SimpleNamespace
from app.api_client import CountryLeadersAPI


class FakeResponse:
    def __init__(self, status_code: int, json_data=None):
        self.status_code = status_code
        self._json_data = json_data or []

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if 400 <= self.status_code:
            raise Exception(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        # responses: dict[url, list[FakeResponse]] to pop sequentially
        self._responses = {k: list(v) for k, v in responses.items()}

    def get(self, url, params=None):
        key = url if params is None else (url, tuple(sorted(params.items())))
        queue = self._responses.get(key) or self._responses.get(url) or []
        if not queue:
            return FakeResponse(404)
        resp = queue.pop(0)
        return resp


def test_get_session_returns_thread_local_instance():
    api = CountryLeadersAPI()

    s1 = api.get_session()
    s2 = api.get_session()
    assert s1 is s2

    results = []

    def other_thread():
        results.append(api.get_session())

    t = threading.Thread(target=other_thread)
    t.start()
    t.join()

    assert results and results[0] is not s1


def test_countries_refreshes_cookie_once_on_401(monkeypatch):
    api = CountryLeadersAPI()

    # Build fake session with 401 then 200 for /countries
    countries_url = api.root_url + api.countries_url
    fake = FakeSession({
        countries_url: [FakeResponse(401), FakeResponse(200, json_data=["A", "B"])],
        api.root_url + api.cookie_url: [FakeResponse(200)],
    })

    monkeypatch.setattr(api, "_get_thread_session", lambda: fake)
    monkeypatch.setattr(api, "_refresh_cookie", lambda s: None)

    countries = api.get_countries()
    assert countries == ["A", "B"]

