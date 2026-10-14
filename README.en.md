# home-inventory-agent

**Create a home contents inventory at replacement value from room videos – with your AI agent.** Every item gets a still image, a price source and a screenshot as proof.

[Deutsche Version](README.md)

## Getting started
Open an AI agent that can read files and run commands (e.g. Claude Code, Codex, Gemini CLI) and type:

```
Download https://github.com/larskohlenberg/home-inventory-agent, read AGENTS.md and guide me through it.
```

The agent sets everything up, explains how to film and tells you after every step what comes next. Works best with a strong model with vision.

## What you get
- `Inventar.xlsx` – one sheet per room plus an overview with totals for contents, building and unclear items; opens in Excel, LibreOffice, Google Sheets and Apple Numbers
- per item: brand/model, quantity, replacement value, location, still from the video, link to the price source, screenshot of the price page
- yellow columns for your corrections – they survive every rebuild

## What you need
- a computer with macOS, Windows or Linux, about 3 GB of free space plus room for the videos
- one smartphone video per room (1–3 minutes) in which you say what you know ("Miele washing machine, 2022, about 1,100 euros")
- internet access for price research

## How it works
1. You film room by room and talk while filming.
2. `tools/prepare_video.py` turns each video into sharp stills and transcribes what you say – locally on your computer.
3. The agent recognises the items and researches current prices.
4. `tools/nachweise.py` takes screenshots of the price pages as proof.
5. `tools/build_excel.py` creates the inventory.
6. You review and correct – in the chat or in the spreadsheet.

The guides in `docs/` and the tool output are in German; your agent translates for you. Outside Germany, Austria and Switzerland, ask the agent to use your local shops and currency.

## Privacy
- Your videos and the speech recognition stay on your computer.
- Stills and photos are sent to your agent's AI model – that is required for recognition.
- Your data lives in a separate project folder outside this repository.

## Disclaimer
Not insurance or legal advice. Prices are estimates based on online offers; check the list yourself. Keep the original videos – they are your evidence.

## License
MIT – see [LICENSE](LICENSE).
