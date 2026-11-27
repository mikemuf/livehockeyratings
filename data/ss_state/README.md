# Live-check state saved for a move to another session (Nov 26, 2026, 7:44 PM Central)
ss_check.py keeps its memory in /tmp, which a new session does not have. Before the first check in a new session:
  mkdir -p /tmp/gs && cp data/ss_state/ss_last.json /tmp/ss_last.json && cp data/ss_state/ss_pk_state.json /tmp/gs/ss_pk_state.json
Then in a NEW Chrome tab on the public scores list (address in data/SS_CHAIN.md): paste tools/ss_list.js (the window.__ssl part), then tools/ss_box.js, run `await window.__ssl('Nov 26')` (or the day), and BEFORE the first __ssgo mark every game that is already final as done and already sent:
  Object.entries(window.__ssraw).forEach(([id,t])=>{const p=t.split(/\(20\d\d\)/);const m=(p[1]||'').match(/^\s*(\d+)\s*[-–]\s*(\d+)(\s+LIVE)?/);if(m&&!m[3]){window.__ssgot[id]=m[1]+'-'+m[2]+'F';window.__ssfr[id]=id+'~'+m[1]+'~'+m[2]+'~FINAL'}})
Otherwise the first check re-reads every finished game (the Nov 26 6:57 PM mistake) and re-sends every final.
tools/ss_box.js reads each game page ONE time (was 3 tries).
tools/tests/ holds the phone-width page testers (t_live.py, t_fin.py, t_fresh.py); they expect /usr/bin/google-chrome and python playwright.
