/*
  Project: wikipedia-scraper
  Purpose: Short guidance for AI coding agents to be immediately productive here.
  Keep this file concise, actionable and specific to patterns discoverable in the repo.
*/

# Copilot instructions for wikipedia-scraper

This repo is a small, notebook-driven scraper that teaches how to query a public API, use the `requests` library, extract/sanitize Wikipedia content, and save results to disk. There are no complex services or CI files — the notebook is the canonical source of truth.

Key files to read first
- `wikipedia_scraper.ipynb` — primary tutorial / implementation. Contains step-by-step cells that describe environment setup, API endpoints, cookie handling, scraping and saving output.
- `README.md` — one-line project title; not authoritative beyond the notebook.

Quick onboarding commands (derived from the notebook)
- Create the venv: `python3 -m venv wikipedia_scraper_env`
- Activate (macOS / zsh): `source wikipedia_scraper_env/bin/activate`
- Install runtime deps (example): `pip install requests`
- Add `wikipedia_scraper_env/` to `.gitignore` if creating the venv locally.

Project-specific patterns and conventions
- Notebook-first: the project is organized as an educational Jupyter notebook. Treat cells as the canonical workflow. If adding scripts, mirror the notebook examples and keep the notebook updated.
- Small-scope scripts: expect short, single-purpose functions (API query, JSON parsing, cookie extraction, HTML scraping, save-to-disk). Prefer clear, small functions over large classes in this repo.
- External API: the notebook queries `https://country-leaders.onrender.com` (endpoints like `/status`, `/countries`, `/leaders`, `/cookie`). Request code should check `status_code` before using `.json()`.
- Cookie handling: the notebook demonstrates fetching a cookie from `/cookie` and re-using it for subsequent requests. Persist cookies in a `requests.Session()` when implementing multiple requests.

Examples to mirror
- API request sanity check (from notebook):
  - Check `resp.status_code == 200` before processing.
  - Use `resp.json()` only after verifying status.
- Save outputs to disk in a small, reproducible format (JSON or CSV). The notebook intends results to be saved for later processing.

What NOT to do
- Do not refactor the notebook into a large framework for this small project. Keep changes minimal and educational.
- Don't assume tests or CI exist — if you add tests, include a short README note explaining how to run them.

When creating PRs
- Update the notebook cells that demonstrate the behavior (notebooks serve as examples).
- Explain changes briefly in the PR body and include a short runnable example (commands to create venv, install deps, and run the notebook or script).

If you need more context
- Inspect `wikipedia_scraper.ipynb` cells that mention the venv name `wikipedia_scraper_env`, `requests`, and the `country-leaders` API. Those cells contain the operational steps and expected checks.

If anything here is unclear or you want me to expand sections (e.g., add sample script templates, or a minimal `requirements.txt`), tell me which parts to expand.
