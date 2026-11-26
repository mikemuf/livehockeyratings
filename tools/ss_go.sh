#!/bin/bash
# tools/ss_go.sh : one live check from the tab's answer. Put the WHOLE answer of `await window.__ssgo(DAY)` ('rows %% deltas') in /tmp/in.txt
# (quoted heredoc), then run this. Prints the last lines of tools/ss_check.py. Optional arg = seconds to sleep afterwards (the wait to the next check).
cd /home/claude/livehockeyratings
A="$(cat /tmp/in.txt | tr -d '\n' | sed 's/<MORE>//g')"; ROWS="${A%% %%*}"; PK="${A#*%% }"; [ "$PK" = "$A" ] && PK=""
timeout 280 python3 tools/ss_check.py "x | $ROWS" "$PK" | grep -v "^upd \|imported\|finals added\|^$" | tail -6
[ -n "$1" ] && sleep "$1"; TZ=America/Chicago date +%H:%M
