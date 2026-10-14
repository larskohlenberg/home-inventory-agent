#!/usr/bin/env python3
"""Screenshots der Preisquellen als Nachweis (Ordner Nachweise/ im Projektordner).

  python tools/nachweise.py pending   <Projektordner> [Raumdatei]  → data/nachweise_pending.json: [{id, url, path}] ohne Screenshot
  python tools/nachweise.py aufnehmen <Projektordner>              → arbeitet nachweise_pending.json im sichtbaren Browser ab
  python tools/nachweise.py apply     <Projektordner> [Raumdatei]  → trägt vorhandene Screenshots als `nachweis` ein

[Raumdatei] = Dateiname in data/raeume/ ohne .json (Präfix genügt), sonst alle Räume.
`aufnehmen` lehnt Cookie-Banner ab, blendet URL + Abrufzeit ein und speichert die oberen 2400 px der Seite.
Blockierte Seiten werden übersprungen, nicht umgangen – dort gelten Link + Preisauszug als Nachweis.
Browser: vorhandenes Chrome oder Edge, sonst Playwright-Chromium (`python -m playwright install chromium`, ca. 150 MB).
Wer ein eigenes Browser-Werkzeug hat, kann statt `aufnehmen` die Liste aus `pending` selbst abarbeiten.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REJECT = re.compile(
    r"^(alle ablehnen|ablehnen|nur (notwendige|erforderliche|essenzielle|technisch notwendige)( cookies)?"
    r"( akzeptieren| zulassen| erlauben| verwenden)?|reject all|decline|weiter ohne (zustimmung|einwilligung)"
    r"|nicht einverstanden|einstellungen ablehnen)$", re.IGNORECASE)
BLOCKED = re.compile(
    r"(access denied|you have been blocked|attention required|captcha|zugriff verweigert|are you a robot"
    r"|bist du ein mensch|403 forbidden|just a moment|seite nicht gefunden|404 not found)", re.IGNORECASE)
# Banner ohne Ablehnen-Knopf nicht akzeptieren, nur für den Screenshot ausblenden
HIDE_BANNERS = """() => {
  const re = /cookie|consent|cmp|privacy|usercentrics|onetrust|didomi|borlabs|klaro|cookiebot/i;
  for (const el of document.querySelectorAll('body *')) {
    const st = getComputedStyle(el);
    if (st.position !== 'fixed' && st.position !== 'sticky') continue;
    const r = el.getBoundingClientRect();
    const big = r.width * r.height > innerWidth * innerHeight * 0.25;
    if (re.test(el.id + ' ' + el.className) || (big && st.position === 'fixed')) el.remove();
  }
  for (const el of document.querySelectorAll('[id*="usercentrics"],#CybotCookiebotDialog,#onetrust-consent-sdk')) el.remove();
  document.documentElement.style.overflow = document.body.style.overflow = 'visible';
}"""
STAMP = """(s) => {
  const d = document.createElement('div');
  d.textContent = s;
  d.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:2147483647;background:#1F3864;color:#fff;' +
    'font:13px/1.6 Arial,sans-serif;padding:4px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis';
  document.body.appendChild(d);
}"""
WIDTH, MAX_HEIGHT = 1280, 2400


def room_files(proj: Path, stem: str):
    return sorted((proj / "data" / "raeume").glob(f"{stem}*.json"))


def pending_and_apply(cmd: str, proj: Path, stem: str):
    out = []
    for f in room_files(proj, stem):
        room = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for p in room["positionen"]:
            if not p.get("preis_url"):
                continue
            rel = f"Nachweise/{room['kuerzel']}/{p['id']}.png"
            if cmd == "pending" and not (proj / rel).exists():
                out.append({"id": p["id"], "url": p["preis_url"], "path": str(proj / rel)})
            elif cmd == "apply" and (proj / rel).exists() and p.get("nachweis") != rel:
                p["nachweis"] = rel
                changed = True
        if changed:
            f.write_text(json.dumps(room, ensure_ascii=False, indent=2), encoding="utf-8")
    if cmd == "pending":
        for o in out:
            Path(o["path"]).parent.mkdir(parents=True, exist_ok=True)
        (proj / "data" / "nachweise_pending.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{len(out)} Screenshots ausstehend → data/nachweise_pending.json")


def launch(pw):
    for channel in ("chrome", "msedge", None):
        try:
            return pw.chromium.launch(channel=channel, headless=False) if channel else pw.chromium.launch(headless=False)
        except Exception:
            continue
    sys.exit("Kein Browser gefunden. Lösung: python -m playwright install chromium  (ca. 150 MB)")


def shoot(page, item) -> str:
    try:
        page.goto(item["url"], wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2500)
        for frame in page.frames:
            btn = frame.get_by_role("button", name=REJECT).first
            try:
                if btn.count() and btn.is_visible():
                    btn.click(timeout=2000)
                    page.wait_for_timeout(800)
                    break
            except Exception:
                continue
        text = page.title() + " " + page.locator("body").inner_text(timeout=5000)[:3000]
        if BLOCKED.search(text):
            return "blockiert/nicht gefunden"
        page.evaluate(HIDE_BANNERS)
        page.evaluate(STAMP, f"{item['id']} · {item['url']} · abgerufen {datetime.now():%d.%m.%Y %H:%M}")
        h = page.evaluate("() => document.documentElement.scrollHeight")
        page.screenshot(path=item["path"], full_page=True, clip={"x": 0, "y": 0, "width": WIDTH, "height": min(h, MAX_HEIGHT)})
        return "ok"
    except Exception as e:
        return "fehler: " + str(e)[:80]


def aufnehmen(proj: Path):
    pending = proj / "data" / "nachweise_pending.json"
    if not pending.exists():
        sys.exit("Erst ausführen: python tools/nachweise.py pending <Projektordner>")
    items = json.loads(pending.read_text(encoding="utf-8"))
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright fehlt. Lösung: pip install -r requirements.txt")
    print("Ein Browserfenster öffnet sich. Bitte nicht schließen – es schließt sich am Ende selbst.", flush=True)
    results = []
    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_context(viewport={"width": WIDTH, "height": 900}, locale="de-DE").new_page()
        for n, item in enumerate(items, 1):
            status = shoot(page, item)
            results.append({"id": item["id"], "status": status})
            print(f"  {n} von {len(items)}: {item['id']} – {status}", flush=True)
        browser.close()
    ok = sum(r["status"] == "ok" for r in results)
    print(f"{ok} von {len(items)} Screenshots gespeichert. Danach: python tools/nachweise.py apply <Projektordner>")


def main():
    for strom in (sys.stdout, sys.stderr):
        strom.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 3 or sys.argv[1] not in ("pending", "aufnehmen", "apply"):
        sys.exit(__doc__)
    cmd, proj = sys.argv[1], Path(sys.argv[2]).resolve()
    if cmd == "aufnehmen":
        aufnehmen(proj)
    else:
        pending_and_apply(cmd, proj, sys.argv[3] if len(sys.argv) > 3 else "")


if __name__ == "__main__":
    main()
