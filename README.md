# home-inventory-agent

**Mit deinem KI-Agenten aus Raumvideos ein Hausratinventar zu Neuwerten erstellen** – mit Standbild, Preisquelle und Screenshot als Nachweis für jeden Gegenstand.

[English version](README.en.md)

## So startest du
Öffne einen KI-Agenten, der Dateien lesen und Befehle ausführen kann (z. B. Claude Code, Codex, Gemini CLI), und schreib:

```
Lade dir https://github.com/larskohlenberg/home-inventory-agent herunter, lies AGENTS.md und führe mich durch.
```

Der Agent richtet alles ein, erklärt dir das Filmen und sagt dir nach jedem Schritt, was als Nächstes kommt. Am besten funktioniert es mit einem starken Modell mit Bildverständnis.

## Was am Ende herauskommt
- `Inventar.xlsx` – je Raum ein Blatt, Übersicht mit Summen für Hausrat, Gebäude und Unklar; öffnet auch in LibreOffice, Google Tabellen und Apple Numbers
- je Gegenstand: Marke/Modell, Anzahl, Neuwert, Fundort, Standbild aus dem Video, Link zur Preisquelle, Screenshot der Preisseite
- gelbe Spalten für deine Korrekturen – sie bleiben beim Neuaufbau erhalten

## Was du brauchst
- Rechner mit macOS, Windows oder Linux, ca. 3 GB freier Platz plus Platz für die Videos
- je Raum ein Smartphone-Video (1–3 Minuten), bei dem du sagst, was du weißt („Miele-Waschmaschine, 2022, etwa 1.100 Euro“)
- Internet für die Preisrecherche

## Wie es funktioniert
1. Du filmst Raum für Raum und sprichst dabei.
2. `tools/prepare_video.py` zerlegt jedes Video in scharfe Einzelbilder und schreibt deine Ansagen mit – lokal auf deinem Rechner.
3. Der Agent erkennt die Gegenstände und recherchiert aktuelle Preise.
4. `tools/nachweise.py` fotografiert die Preisseiten als Nachweis.
5. `tools/build_excel.py` erstellt die Inventarliste.
6. Du prüfst und korrigierst – im Chat oder in der Tabelle.

Entstanden ist das Vorgehen bei der Inventur eines Einfamilienhauses (17 Räume, rund 870 Positionen).

## Datenschutz
- Deine Videos und die Spracherkennung bleiben auf deinem Rechner.
- Einzelbilder und Fotos werden an das KI-Modell deines Agenten geschickt – das ist für die Erkennung nötig.
- Deine Daten liegen in einem eigenen Projektordner außerhalb dieses Repos.

## Haftung
Keine Versicherungs- oder Rechtsberatung. Die Preise sind Schätzungen auf Basis von Online-Angeboten; prüfe die Liste selbst. Bewahre die Originalvideos auf – sie sind dein Nachweis.

## Lizenz
MIT – siehe [LICENSE](LICENSE).
