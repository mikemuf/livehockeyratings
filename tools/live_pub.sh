#!/bin/bash
# tools/live_pub.sh "commit message"  : after gs_import + edits; stamps the update time, builds, checks, publishes. Stops at the first failure.
set -e
cd /home/claude/livehockeyratings
python3 tools/gs_fix.py
python3 tools/dh_mark.py
python3 - <<'P'
import json,datetime,zoneinfo
W=json.load(open('data/weekend_public.json'))
W['updated']=datetime.datetime.now(zoneinfo.ZoneInfo('America/Chicago')).strftime('%a %b %-d, %-I:%M %p')+' CT'
json.dump(W,open('data/weekend_public.json','w'),ensure_ascii=False,indent=1)
P
python3 build/build.py >/dev/null
git checkout build/__pycache__ 2>/dev/null || true
# current ratings -> player/data/ratings.json, refresh rank/rating mentions in the Weekend text, then check (Nov 20, 2026: the check had been reading a stale ratings.json)
(cd /home/claude/player/data && node ../build/ratings_from_site.js /home/claude/livehockeyratings/index.html ratings.json >/dev/null)
(cd /home/claude/player && python3 build/weekend_refresh.py && python3 build/weekend_check.py | tail -1 | grep -q '^OK')
python3 build/build.py >/dev/null
git checkout build/__pycache__ 2>/dev/null || true
git add -A
git commit -qm "$1

Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01VFEdd2WZ5V98gBRHcarm83"
git push -q
/home/claude/player/build/ratings_to_site.sh | tail -1
python3 tools/live_gaps.py || true
