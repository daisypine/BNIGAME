# BNI Premiere — weekly rotation runbook

Everything needed to rebuild bnipremierchapter.com lives in this repo (daisypine/BNIGAME, GitHub Pages, branch `main`).
This `_tools/` folder is not published (Jekyll skips folders starting with `_`).

## Sources of truth
- **Speaker rotation sheet:** Google Sheet `1c9tv3bGZbPjgRE6ds9JgKbizF-U4Z5kMNx_O7q_79MM`, tab `Rotation`.
  Columns: A First, B Last, C Email, D MSP, E Passport, F Last Presented (e.g. "Oct 28, 2026"), G Days Since (formula), H Next Scheduled (e.g. "Nov 4"), I Confirmed, J Backup, K Status (formula).
- **Speaker schedule on the site:** the `SPEAKERS` list in `build_site.py` (dates YYYY-MM-DD, names exactly as in the member directory, e.g. "Clifford Shaw", "Robert Min", "Ramji Digumarthi", "Sailosi Taunaholo", "Felipe Miguel Mejia").
- **BAND events:** https://www.band.us/band/95667588/event (BNI-Premiere SJ group calendar).
- **Per-meeting agenda extras:** `agenda_config.json` keyed by meeting date: `{"tyfcb": true, "events": [{"date","title","time","place","host"}]}`.
- **Agenda list:** `agendas.json` — `[{"date":"2026-10-28","slug":"october28"}, ...]`.

## Builds (run from `_tools/`; `SITE` defaults to the repo root)
- Website:      `python3 build_site.py source-index.html bni-logo.png ../index.html`
- Agenda:       `python3 build_agenda.py bni-logo.png ../agenda/<slug>/index.html <YYYY-MM-DD> ../../`
- Agenda list:  `python3 build_agenda_index.py bni-logo.png ../agenda/index.html`
- IG flyers:    `python3 make_flyers.py <YYYY-MM-DD> "Name 1" "Name 2" "Name 3"` → `../flyers/<mon><day>-story.png` and `-feed.png`
Needs: `pip install qrcode playwright` (Chromium already present in Claude's cloud workspace).
Slug format: full lowercase month + day, e.g. `november4`, `december16`, `january6`.
Never rebuild a past meeting's agenda — those are frozen archives.

## The site rolls over by itself
The homepage shows a meeting as "this week" until 8:30 AM on meeting day, then automatically switches to the next week. No rebuild needed for that.

## Wednesday after the meeting (9:00 AM)
1. Sheet: for today's speakers set F = today ("Mmm D, YYYY") and clear H. Don't touch formula columns G and K.
2. If the sheet's Next Scheduled dates disagree with `SPEAKERS` in `build_site.py`, the sheet wins: update `SPEAKERS`, rebuild the website.
3. Next week's agenda: read BAND events for the next ~3 weeks, add them to `agenda_config.json` under next meeting's date (keep `"tyfcb": true` only if asked), add the meeting to `agendas.json`, build the agenda and the agenda list.
4. Flyers for next week's 3 speakers with `make_flyers.py`.
5. Commit + push to `main` (`_tools/` changes too, so state carries over). Wait ~60 s and check the live pages.
