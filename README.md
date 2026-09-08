# Champions League Dashboard 2026/27

Live league-phase table, matchday results, trends and full match log. Static site, refreshed by a GitHub Action.

## Setup (once, about 5 minutes)

1. Create a new public GitHub repo (e.g. `ucl-dashboard`) and push these files.
2. Get a free API key at https://www.football-data.org/client/register (free tier covers the Champions League).
3. In the repo: Settings > Secrets and variables > Actions > New repository secret
   Name: `FOOTBALL_DATA_TOKEN`, value: your key.
4. Settings > Pages > Source: Deploy from a branch, branch `main`, folder `/ (root)`.
5. Actions tab > "Update Champions League data" > Run workflow. This writes the first `data.json`.

Your dashboard is then live at `https://<your-username>.github.io/ucl-dashboard/` and refreshes every 6 hours, hourly on match nights.

## Files

- `index.html` - the dashboard. Loads `data.json`; falls back to an embedded snapshot if missing.
- `fetch_data.py` - pulls matches from football-data.org and writes `data.json`.
- `.github/workflows/update.yml` - the schedule.
- `data.json` - current data (auto-committed by the Action).

## Notes

- Pre-match win probabilities are not in the free API, so they only appear in the embedded snapshot.
- To point at a later season, set the `CL_SEASON` env var in the workflow (e.g. `2027`).
