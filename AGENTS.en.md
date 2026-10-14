# AGENTS.en.md – Instructions for AI agents

> Deutsch: [AGENTS.md](AGENTS.md). Always talk to the user in their language.

This repository lets you guide a person without prior knowledge to a complete **home contents inventory**: every item with replacement value (today's price for an equivalent item), still image, price source and a screenshot as proof. Purpose: check the insured sum and prove what existed in case of a claim. This is not insurance advice.

You work independently: you keep track of what is done and what is missing, find duplicates, apply corrections and solve problems yourself. The tools in `tools/` handle the technical parts; everything else is up to you – with your own small helper scripts if needed.

**Language note:** the guides in `docs/` and the tool output are in German. Read them and explain everything to the user in their language. Outside Germany, Austria and Switzerland use local shops and the local currency for prices.

## Rules
1. **Explain before you act.** Before each step, say in plain words what you do and why. Name download sizes. Never estimate minutes – say "this takes a while" at most and pass on the progress messages of the tools.
2. **Announce permission prompts.** Your program may ask the user whether you may run a command, write a file or open a web page. Say so beforehand, e.g. "Your program will now ask whether I may prepare the video. I will split it into stills and transcribe what you said. Please allow it." If the user declines, ask how they want to continue.
3. **Always name the next step.** After every step: what is done and what comes next – including what the user has to do.
4. **The user has priority.** Order of sources: user statement > receipt > spoken note in the video > your image recognition > estimate. If the user says "that is actually …", "it cost …" or "leave that out, it's nobody's business", apply it without discussion.
5. **The transcript is automatic.** If a word sounds like a known brand and fits image and context, correct it yourself and note it. Ask only if speech and image really contradict each other.
6. **Do not change the tools in this repository.** Put your own helper scripts into the project folder (e.g. `.work/skripte/`), never into the repository.
7. **Privacy.** The user's project folder lives **outside** this repository – user data never goes into the repository. Tell the user honestly at the start: stills and photos are sent to you (the AI model); videos and speech recognition stay on their computer.
8. **Save progress.** Write room files right after recognition and update them during price research. The user may keep filming while you work.

## Workflow
1. **Welcome:** what the result is (Inventar.xlsx with photos, prices and proofs), what the user has to do (one video per room, talk while filming), privacy (rule 7).
2. **Set up** – commands per operating system below. Check Python 3.10 or newer, create a virtual environment, install `requirements.txt` (about 300–500 MB). The speech model (about 1.6 GB) is downloaded automatically by `prepare_video.py` on first use – announce it.
3. **Create the project folder** outside the repository, e.g. `Documents/Home-Inventory/` with subfolders `Videos/`, `Fotos/`, `Belege/`, `data/raeume/`, `Standbilder/`, `Nachweise/`. Ask for key facts: type of home, recording date, threshold for single items (default 50 €), quality assumption (default upper mid-range brands). Write them to `project folder/projekt.md`.
4. **Explain filming** following [docs/filmen.md](docs/filmen.md) – including the example sentences. Then wait until the user reports that videos are ready. Pass `--sprache en` (or the user's language) to `prepare_video.py` if they do not speak German.
5. **Per video:** `tools/prepare_video.py` → evaluate the room following [docs/raum-auswerten.md](docs/raum-auswerten.md) → short summary for the user.
6. **Across rooms:** check duplicates, evaluate photos of valuables, match receipts.
7. **Proofs:** `tools/nachweise.py pending` → `aufnehmen` → `apply`; review the screenshots (covered? price visible and equal?).
8. **Inventory:** `tools/build_excel.py` → walk through it with the user, explain the yellow correction columns, apply corrections.

Overall process and rules: [docs/vorgehen.md](docs/vorgehen.md).

## Setup per operating system
Run inside the repository folder:

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Check Python | `python3 --version` | `py --version` |
| Python missing | python.org or `brew install python@3.12`; Linux: `sudo apt install python3 python3-venv` | `winget install -e --id Python.Python.3.12` |
| Environment | `python3 -m venv .venv` | `py -m venv .venv` |
| Install | `.venv/bin/pip install -r requirements.txt` | `.venv\Scripts\pip install -r requirements.txt` |
| Run a tool | `.venv/bin/python tools/…` | `.venv\Scripts\python tools\…` |

If installation fails with a very new Python version, use Python 3.12.

## Tools
| Command | Purpose |
|---|---|
| `python tools/prepare_video.py <project>/Videos/<name>.MOV` | stills (1/s, sharpest of 3), contact sheets, transcript → `<project>/.work/<name>/` |
| `python tools/nachweise.py pending <project> [room]` | list of price pages without screenshot |
| `python tools/nachweise.py aufnehmen <project>` | screenshots in a visible browser (cookie banners are declined) |
| `python tools/nachweise.py apply <project> [room]` | register the screenshots in the room files |
| `python tools/build_excel.py <project>` | create `Inventar.xlsx`; corrections in the yellow columns are kept |

No browser for screenshots? Either `python -m playwright install chromium` (about 150 MB) or let your own browser tool work through the list from `pending`. If neither works, link, price excerpt and retrieval date serve as proof.

## Saving cost
If you can start sub-agents with their own model choice, hand clearly scoped tasks to cheaper models so the user's usage limits last:

| Task | Model |
|---|---|
| Guiding the user, questions, duplicates, corrections | you |
| Evaluating a room (recognising items in images) | mid-tier with vision – completeness happens here |
| Price research for already named items | cheapest model with web search |
| Reviewing screenshots, reading receipts | cheap, with vision |

Give each sub-agent the matching guide (docs/raum-auswerten.md) and exactly the files it needs. Sub-agents do not use a browser and never set the field `nachweis`; parallel sub-agents each get their own room and notes folder. Check their results before you continue.
