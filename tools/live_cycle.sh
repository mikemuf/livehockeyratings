#!/bin/bash
# tools/live_cycle.sh "id~vs~hs~st ## ..." [PKFILE] : one live-score cycle. With PKFILE (window.__pk lines saved to a file) the games get the FULL
# sheet (goals, scorers, period scores) through tools/live_full.py; the ~ lines still update plain scores. Then publish, show finals and gaps.
cd /home/claude/livehockeyratings
[ -n "$2" ] && python3 tools/live_full.py "$2"
python3 tools/live_auto.py "$1" | grep -v "^upd " 
tools/live_pub.sh "live refresh $(date +%H:%M)" 2>&1 | grep "NO LIVE\|live gaps\|published" | cut -c1-120
date +%H:%M
