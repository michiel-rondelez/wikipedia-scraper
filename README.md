# wikipedia-scraper
Wikipedia scraper





## Optimaztion of my solution



Process completed successfully!
==================================================
Time taken to get all leaders: 1.5496060848236084 seconds
Time taken to add Wikipedia paragraphs: 17.183464288711548 seconds
Total time taken: 18.733084201812744 seconds
==================================================


Precompute and skip work
Deduplicate leaders by wikipedia_url and reuse the paragraph: map url -> paragraph to avoid repeated fetches.
Skip leaders without wikipedia_url up front.
Reduce asymptotic work
Fetch leaders per country once; avoid recomputing the countries list or re-calling on retries unnecessarily.
If the API can return “all leaders,” prefer one bulk call over per-country loops.
Cache results
Persist a local cache (JSON/SQLite) keyed by leader_id or wikipedia_url. On reruns, only fetch missing entries.
Make parsing cheaper
Precompile regex in clean_text.
Use a single targeted selector (e.g., first non-empty p, then early-exit on first match with bold name).
Control flow efficiency
Short-circuit: if a page returns 403/404, don’t retry that URL in the same run.
Batch save: write results incrementally (append or chunked) to avoid holding everything in memory.
Robust retries
Exponential backoff with capped retries and a retry budget per URL to prevent pathological time sinks.






