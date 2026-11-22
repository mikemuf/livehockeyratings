#!/bin/bash
# tools/live_cycle.sh "id~vs~hs~st ## ..."  : one live-score cycle: update scores of games already in the box, publish, show new finals and gaps.
cd /home/claude/livehockeyratings
python3 tools/live_auto.py "$1" | grep -v "^upd " 
tools/live_pub.sh "live refresh $(date +%H:%M)" 2>&1 | grep "NO LIVE\|live gaps\|published" | cut -c1-120
date +%H:%M
