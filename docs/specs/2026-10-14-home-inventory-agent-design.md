# home-inventory-agent – Design (Version 1, schlank)

Stand: 14.10.2026

## Ziel
Öffentliches Repo `larskohlenberg/home-inventory-agent` (MIT), mit dem ein KI-Agent aus Raumvideos ein Hausratinventar zu Neuwerten erstellt – so, wie es im Pilotprojekt funktioniert hat. Einstieg für den Nutzer:

> Lade dir https://github.com/larskohlenberg/home-inventory-agent herunter, lies AGENTS.md und führe mich durch.

## Grundannahme
Der Agent ist fähig: Er behält den Überblick über den Stand, findet Dubletten, pflegt Korrekturen ein, löst Probleme selbst und darf sich dafür Hilfsskripte im Projektordner schreiben. Das Repo liefert nur das, was sich im Pilot bewährt hat, plus Anleitung – keine zusätzliche Steuerungslogik.

## Umfang Version 1
- **Werkzeuge** (aus dem Pilot übernommen, entschärft): `tools/prepare_video.py` (Einzelbilder, Kontaktbögen, Transkript), `tools/build_excel.py` (Inventar.xlsx mit Korrekturspalten), `tools/nachweise.py` (offene Screenshots ermitteln, im Browser aufnehmen, eintragen).
  - keine festen Pfade: Projektordner als Argument bzw. aktueller Ordner
  - läuft auf macOS, Linux, Windows: faster-whisper statt whisper.cpp, ffmpeg aus dem System oder `imageio-ffmpeg`, Pillow-Standardschrift
  - Screenshots per Python-Playwright im sichtbaren Browser (vorhandenes Chrome/Edge, sonst Chromium) statt Claude-eigenem Browser-Werkzeug
- **Anleitung**: `AGENTS.md` (DE) und `AGENTS.en.md`, `docs/vorgehen.md`, `docs/filmen.md` (inkl. „Beim Filmen sprechen“), `docs/raum-auswerten.md` (verallgemeinerte Raum-Anleitung inkl. Erkenntnisse aus dem Pilot).
- **README** DE + EN mit Start-Prompt, Voraussetzungen, Datenschutz, Haftung.

## Leitplanken in AGENTS.md
- Vor jeder Aktion erklären, was passiert und warum; Freigabe-Abfragen des Programms vorher ankündigen; Download-Größen nennen, keine Minutenschätzungen.
- Nach jedem Schritt sagen, was als Nächstes kommt.
- Nutzer hat Vorrang (Nutzer > Beleg > Ansage > Bilderkennung > Schätzung); Ausschlüsse („geht niemanden etwas an“) werden umgesetzt.
- Transkript ist eine automatische Abschrift: ähnlich klingende Marken selbst korrigieren, nur bei echtem Widerspruch nachfragen.
- Werkzeuge im Repo nicht ändern; Hilfsskripte nur im Projektordner.
- Projektordner liegt außerhalb des Repos; Datenschutz ehrlich erklären.
- Kosten sparen: wenn möglich Unteragenten mit günstigen Modellen für klar umrissene Aufgaben (Raum auswerten: mittel mit Bildverständnis; Preisrecherche: günstigstes Modell mit Websuche).

## Später (Version 1.1, nur bei Bedarf)
Belege/Rechnungen als eigener Ablauf, CSV-Ausgabe, Dubletten-Werkzeug, Änderungsbefehle, Prüf- und Statusbefehle, Zählhilfe, Detailbild-Befehl, automatische Tests auf drei Systemen, Beispielraum.

## Datenschutz und Haftung
Keine Versicherungs- oder Rechtsberatung; Preise sind Schätzungen. Einzelbilder gehen an das KI-Modell, Videos und Spracherkennung bleiben lokal. Nutzerdaten nie ins Repo.
