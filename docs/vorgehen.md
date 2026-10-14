# Vorgehen – Hausratinventar aus Raumvideos

## Ziel
Vollständige Inventarliste aller Gegenstände zu **Neuwert** (heutiger Wiederbeschaffungspreis), um
1. die Versicherungssumme zu prüfen und
2. im Schadensfall nachzuweisen, was vorhanden war.

Ein Abgleich mit Tarifgrenzen einzelner Versicherungsangebote gehört nicht dazu.

## Ablauf
1. **Filmen** (Nutzer) – siehe [filmen.md](filmen.md).
2. **Vorbereiten** – `tools/prepare_video.py`: scharfe Einzelbilder (1/s), Kontaktbögen, Transkript (lokal).
3. **Auswerten** – je Video nach [raum-auswerten.md](raum-auswerten.md) → `data/raeume/<Video>.json` + `Standbilder/`.
4. **Preisnachweise** – `tools/nachweise.py pending` → `aufnehmen` → `apply` → `Nachweise/`.
5. **Inventar** – `tools/build_excel.py` → `Inventar.xlsx`.
6. **Korrekturen** – Nutzer prüft, korrigiert im Chat oder in den gelben Spalten; Agent arbeitet ein und baut neu.

## Regeln
- **Einzelposition** ab der vereinbarten Grenze (Standard **50 €** Neuwert), jeweils mit **Online-Preisquelle** (Link, Datum, Auszug, Screenshot).
- Darunter: **Sammelposten** pro Raum.
- **Kleidung:** pro Schrank/Kategorie geschätzt (Stückzahl × Markenpreis).
- **Qualitätsannahme:** wie vereinbart (Standard gehobene Markenqualität); unbekanntes Modell → „Modell unklar – bitte prüfen“.
- **Zuordnung** je Position: **Hausrat / Gebäude / Unklar** – alles wird erfasst, in die Hausratsumme zählt nur „Hausrat“.
- **Dubletten** über Videos hinweg nur einmal zählen.
- **Stichtagsprinzip:** gezählt wird, was im jeweiligen Video zu sehen ist, nicht „wo es eigentlich hingehört“.
- **Rangfolge der Quellen:** Nutzer > Rechnung > Ansage > Bilderkennung > Schätzung.
- **Neuwert** = gleichwertiges heutiges Modell; darf unter dem alten Kaufpreis liegen. Der Nutzer darf ein Nachfolgemodell wählen. Nennt er einen Kaufpreis, gilt dieser als Preisquelle.

## Korrekturen
- **Im Chat:** Der Agent ändert die Position in der Raumdatei (per ID, nie per Stichwort – sonst trifft man Falsches) und ergänzt im Hinweis „laut Nutzer bestätigt“.
- **In Inventar.xlsx:** gelbe Spalten ausfüllen (Korr. Marke/Modell, Korr. Preis, Korr. Anzahl, Korr. Zuordnung, Löschen (x), Geprüft (x), Bemerkung), Datei schließen, Agent Bescheid sagen. `build_excel.py` übernimmt die Einträge und sichert sie in `data/korrekturen.json`; sie gehen beim Neuaufbau nie verloren.
- Bei geändertem Modell recherchiert der Agent den Preis neu. Ändert sich die Preis-URL, wird der alte Screenshot entfernt und neu aufgenommen.
- **„Das geht niemanden etwas an“:** Position aus der Raumdatei entfernen und in `data/ausgeschlossen.json` notieren, damit sie bei einer erneuten Auswertung nicht wieder auftaucht.

## Ordner im Projektordner
| Ordner/Datei | Inhalt |
|---|---|
| `Videos/` | Originalvideos (Beweismittel – aufbewahren!) |
| `Fotos/<Thema>/` | Einzelfotos von Wertsachen, Sammlungen, Kunst |
| `Belege/` | Rechnungen als Foto oder PDF |
| `Inventar.xlsx` | Ergebnisliste |
| `Standbilder/<Kürzel>/` | Bild je Position |
| `Nachweise/<Kürzel>/` | Screenshots der Preisquellen |
| `data/raeume/` | Rohdaten je Video (JSON) |
| `data/korrekturen.json` | Sicherung der Tabellen-Korrekturen |
| `.work/` | Einzelbilder, Kontaktbögen, Transkripte, Hilfsskripte des Agenten |
