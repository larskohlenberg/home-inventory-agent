# AGENTS.md – Anleitung für KI-Agenten

> English: [AGENTS.en.md](AGENTS.en.md). Sprich mit dem Nutzer immer in seiner Sprache.

Mit diesem Repo führst du einen Menschen ohne Vorwissen zu einer vollständigen **Hausrat-Inventarliste**: jeder Gegenstand mit Neuwert (heutiger Wiederbeschaffungspreis), Standbild, Preisquelle und Screenshot als Nachweis. Zweck: die Versicherungssumme prüfen und im Schadensfall belegen, was vorhanden war. Das ist keine Versicherungsberatung.

Du arbeitest selbstständig: Du behältst den Überblick, was erledigt ist und was fehlt, findest Dubletten, pflegst Korrekturen ein und löst Probleme selbst. Die Werkzeuge in `tools/` nehmen dir die Technik ab; alles andere machst du – bei Bedarf mit eigenen kleinen Hilfsskripten.

## Regeln
1. **Erst erklären, dann ausführen.** Vor jedem Schritt sagst du in einfachen Worten, was du tust und wozu. Bei Downloads nennst du die Größe. Nenne keine Minutenangaben – sag höchstens „das dauert eine Weile“ und gib die Fortschrittsmeldungen der Werkzeuge weiter.
2. **Freigabe-Abfragen ankündigen.** Dein Programm fragt den Nutzer womöglich, ob du einen Befehl ausführen, eine Datei schreiben oder eine Webseite öffnen darfst. Sag das vorher, z. B.: „Gleich fragt dich dein Programm, ob ich das Video vorbereiten darf. Dabei zerlege ich es in Einzelbilder und schreibe deine Ansagen mit. Bitte erlauben.“ Lehnt der Nutzer ab, frag, wie er weitermachen möchte.
3. **Immer den nächsten Schritt nennen.** Nach jedem Schritt: kurz, was erledigt ist, und was als Nächstes kommt – auch, was der Nutzer tun muss.
4. **Der Nutzer hat Vorrang.** Rangfolge: Angabe des Nutzers > Rechnung > Ansage im Video > deine Bilderkennung > Schätzung. Sagt der Nutzer „das ist eigentlich …“, „hat … gekostet“ oder „das nehmen wir raus, geht niemanden etwas an“, übernimmst du das ohne Diskussion.
5. **Das Transkript ist eine automatische Abschrift.** Klingt ein Wort wie eine bekannte Marke und passt es zu Bild und Zusammenhang („Knurps“ → Knirps, „Sonnens“ → Sonos), korrigierst du es selbst und vermerkst es im Hinweis. Nachfragen nur, wenn Ansage und Bild sich wirklich widersprechen.
6. **Werkzeuge im Repo nicht ändern.** Eigene Hilfsskripte legst du im Projektordner ab (z. B. `.work/skripte/`), nie im Repo.
7. **Datenschutz.** Der Projektordner des Nutzers liegt **außerhalb** dieses Repos – Nutzerdaten kommen nie ins Repo. Sag dem Nutzer zu Beginn ehrlich: Einzelbilder und Fotos werden an dich (das KI-Modell) geschickt; Videos und Spracherkennung bleiben auf seinem Rechner.
8. **Zwischenstände sichern.** Schreibe Raumdateien sofort nach dem Erkennen und aktualisiere sie während der Preisrecherche. Der Nutzer darf weiterfilmen, während du auswertest.

## Ablauf
1. **Begrüßen:** Was am Ende herauskommt (Inventar.xlsx mit Fotos, Preisen und Nachweisen), was der Nutzer tun muss (je Raum ein Video, dabei sprechen), Datenschutz (Regel 7).
2. **Einrichten** – Befehle je Betriebssystem siehe unten. Python 3.10 oder neuer prüfen, virtuelle Umgebung anlegen, `requirements.txt` installieren (ca. 300–500 MB). Das Sprachmodell (ca. 1,6 GB) lädt `prepare_video.py` beim ersten Mal automatisch – vorher ankündigen.
3. **Projektordner anlegen** – außerhalb des Repos, z. B. `Dokumente/Hausrat-Inventar/` mit den Unterordnern `Videos/`, `Fotos/`, `Belege/`, `data/raeume/`, `Standbilder/`, `Nachweise/`. Eckdaten erfragen: Wohnform (Haus/Wohnung, Miete/Eigentum), Tag der Aufnahmen, Grenze für Einzelpositionen (Standard 50 €), Qualitätsannahme (Standard gehobene Markenqualität). Notiere sie in `Projektordner/projekt.md`.
4. **Filmen erklären** nach [docs/filmen.md](docs/filmen.md) – mit den Beispielsätzen zum Sprechen. Dann warten, bis der Nutzer meldet, dass Videos da sind.
5. **Je Video:** `tools/prepare_video.py` → Raum auswerten nach [docs/raum-auswerten.md](docs/raum-auswerten.md) → kurze Rückmeldung an den Nutzer.
6. **Über alle Räume:** Dubletten prüfen (Abschnitt in docs/raum-auswerten.md), Wertsachen-Fotos auswerten, Rechnungen zuordnen.
7. **Nachweise:** `tools/nachweise.py pending` → `aufnehmen` → `apply`; Screenshots sichten (verdeckt? Preis sichtbar und gleich?).
8. **Inventar:** `tools/build_excel.py` → mit dem Nutzer durchgehen, gelbe Korrekturspalten erklären, Korrekturen einarbeiten.

Gesamtablauf und Regeln: [docs/vorgehen.md](docs/vorgehen.md).

## Einrichten je Betriebssystem
Im Repo-Ordner ausführen:

| | macOS / Linux | Windows (PowerShell) |
|---|---|---|
| Python prüfen | `python3 --version` | `py --version` |
| Python fehlt | python.org oder `brew install python@3.12`; Linux: `sudo apt install python3 python3-venv` | `winget install -e --id Python.Python.3.12` |
| Umgebung | `python3 -m venv .venv` | `py -m venv .venv` |
| Installieren | `.venv/bin/pip install -r requirements.txt` | `.venv\Scripts\pip install -r requirements.txt` |
| Werkzeug starten | `.venv/bin/python tools/…` | `.venv\Scripts\python tools\…` |

Scheitert die Installation mit einer sehr neuen Python-Version, Python 3.12 verwenden.

## Werkzeuge
| Aufruf | Wozu |
|---|---|
| `python tools/prepare_video.py <Projekt>/Videos/<Name>.MOV` | Einzelbilder (1/s, schärfstes von 3), Kontaktbögen, Transkript → `<Projekt>/.work/<Name>/` |
| `python tools/nachweise.py pending <Projekt> [Raum]` | Liste der Preisseiten ohne Screenshot |
| `python tools/nachweise.py aufnehmen <Projekt>` | Screenshots im sichtbaren Browser (Cookie-Banner werden abgelehnt) |
| `python tools/nachweise.py apply <Projekt> [Raum]` | Screenshots in die Raumdateien eintragen |
| `python tools/build_excel.py <Projekt>` | `Inventar.xlsx` erstellen; Korrekturen aus den gelben Spalten bleiben erhalten |

Kein Browser für Screenshots vorhanden? Entweder `python -m playwright install chromium` (ca. 150 MB) oder dein eigenes Browser-Werkzeug die Liste aus `pending` abarbeiten lassen. Geht beides nicht, gelten Link, Preisauszug und Abrufdatum als Nachweis.

## Kosten sparen
Kannst du Unteragenten mit eigener Modellwahl starten, gib klar umrissene Aufgaben an günstigere Modelle ab, damit die Nutzungslimits des Nutzers nicht schnell aufgebraucht sind:

| Aufgabe | Modell |
|---|---|
| Nutzerführung, Rückfragen, Dubletten, Korrekturen | du selbst |
| Raum auswerten (Gegenstände in Bildern erkennen) | mittel, mit Bildverständnis – hier entsteht die Vollständigkeit |
| Preisrecherche für fertig benannte Gegenstände | günstigstes Modell mit Websuche |
| Screenshots sichten, Rechnungen lesen | günstig, mit Bildverständnis |

Gib jedem Unteragenten die passende Anleitung (docs/raum-auswerten.md) und genau die Dateien, die er braucht. Unteragenten benutzen keinen Browser und setzen kein Feld `nachweis`; parallele Unteragenten bekommen je einen eigenen Raum und eigenen Notizordner. Prüfe ihre Ergebnisse, bevor du weitermachst.
