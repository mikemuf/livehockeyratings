# When to run live checks (Mike, Sun Nov 15 10:31 PM)

Mike wants the check frequency to follow the games, not the clock. No runs when nothing is happening.

## The weekend planner (scheduled task "Weekend live-ratings check", Sat & Sun 7:12 AM CT)
Each planner run:
1. Builds the day's list of tracked games with start times in Central. Sources:
   - The weekend file (data/weekend_*.txt) and the schedule files.
   - The tournament schedules and GameSheet lists.
   - MHR PREVIEW lines for top-25 teams.
   - The Reapers/Mission accounts.
2. If there are no tracked games that day, it sends one short line ("No tracked games today") and stops.
3. Otherwise it uses send_later for the first check at the first game's start + 15 min. It sends no score message at this point. The final reply is only a one-line plan, e.g. "Today: first puck 8:30 AM — live checks start 8:45."

## Live checks (send_later chain)
- Run every 15 min while any tracked game is in progress or starts within 30 min.
- Run every 5 min during tournament semifinals and championship games.
- Gap rule: if no game is live and the next start is more than 45 min away, schedule the next check for that start time + 15 min. Do not run during idle gaps.
- After the day's last tracked game is final:
  - Post the day's wrap-up message.
  - Stop the chain. No more runs that day.
- Late results:
  - At most one "late results" sweep, ~2 hours after the last game (MHR top-25 scan for that date).
  - Only message if something new was added.
- Sunday after the sweep: nothing more until the Wednesday MHR update.

## Friday evening games
The Wednesday MHR update builds the weekend schedule. If tracked teams play Friday, it sets a send_later for Friday at the first start + 15 min.

## Messages
- The final reply of every run reaches Mike. It is a short score or news update only.
- If a check finds nothing new, keep it to one line.
- Avoid scheduling a check that is likely to find nothing new.

## Nov 18, 2026: everything runs in one conversation now
Mike moved all live-ratings work into the player-database conversation. The Wednesday MHR update, the Saturday/Sunday 7:12 AM planner and the Friday live checks are now send_later chains in that conversation; each run schedules its own next run first. The old scheduled tasks of the same names are switched off. Reports link https://myplayerdata.com only, never the mikemuf.github.io address.
