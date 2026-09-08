"""Pull Champions League 2026/27 league-phase matches from football-data.org
and write data.json for index.html.

Requires env var FOOTBALL_DATA_TOKEN (free key from https://www.football-data.org/client/register).
No third-party packages needed.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

TOKEN = os.environ.get("FOOTBALL_DATA_TOKEN")
if not TOKEN:
    sys.exit("FOOTBALL_DATA_TOKEN is not set")

SEASON = os.environ.get("CL_SEASON", "2026")
URL = f"https://api.football-data.org/v4/competitions/CL/matches?season={SEASON}"

req = urllib.request.Request(URL, headers={"X-Auth-Token": TOKEN})
with urllib.request.urlopen(req, timeout=30) as r:
    payload = json.load(r)

STATUS = {
    "FINISHED": "final",
    "IN_PLAY": "live",
    "PAUSED": "live",
    "SUSPENDED": "live",
}

teams, matches = {}, []
for m in payload.get("matches", []):
    if m.get("stage") != "LEAGUE_STAGE":
        continue
    h, a = m["homeTeam"], m["awayTeam"]
    for t in (h, a):
        if t.get("tla"):
            teams[t["tla"]] = t.get("shortName") or t.get("name")
    status = STATUS.get(m["status"], "scheduled")
    row = {
        "md": m.get("matchday"),
        "t": m["utcDate"],
        "h": h.get("tla"),
        "a": a.get("tla"),
        "status": status,
    }
    ft = (m.get("score") or {}).get("fullTime") or {}
    if status != "scheduled":
        row["hs"] = ft.get("home") if ft.get("home") is not None else 0
        row["as"] = ft.get("away") if ft.get("away") is not None else 0
    if row["md"] and row["h"] and row["a"]:
        matches.append(row)

# Keep only matchdays that have started or are next up, so the hero shows the right round.
matches.sort(key=lambda x: (x["md"], x["t"]))
played_mds = {x["md"] for x in matches if x["status"] != "scheduled"}
next_md = min([x["md"] for x in matches if x["status"] == "scheduled"] or [0])
keep = played_mds | ({next_md} if next_md else set())
matches = [x for x in matches if x["md"] in keep]

out = {
    "asof": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "season": SEASON,
    "teams": dict(sorted(teams.items())),
    "matches": matches,
}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"Wrote data.json: {len(teams)} teams, {len(matches)} matches, matchdays {sorted(keep)}")
