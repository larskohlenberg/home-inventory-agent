# Ein Raumvideo inventarisieren

Diese Anleitung gilt für den Agenten bzw. einen Unteragenten, der genau einen Raum auswertet. `PROJ` = Projektordner des Nutzers. Eckdaten (Grenze für Einzelpositionen, Qualitätsannahme, Wohnform) stehen in `PROJ/projekt.md`.

## Eingaben
- Video `PROJ/Videos/<Name>.MOV` (Dateiname = Raum_Etage)
- Vorbereitete Daten in `PROJ/.work/<Name>/` (sonst erst `python tools/prepare_video.py PROJ/Videos/<Name>.MOV`):
  - `sheets/sheet_NN.jpg` – Kontaktbögen, 6 Bilder je Bogen, gelber Zeitstempel oben links
  - `frames/tMMmSSs.jpg` – Einzelbilder pro Sekunde (720 px breit) für den Detailblick
  - `transcript.txt` – Ansagen des Nutzers mit Zeitstempel (Marke, Kaufjahr, Preis, Mengen …)
- Für Details (Typenschild, Signatur) ein Bild in voller Auflösung ziehen: `ffmpeg -ss <Sekunde> -i <Video> -frames:v 1 -q:v 2 detail.jpg` (optional mit `-vf crop=b:h:x:y`). ffmpeg liegt im System oder unter `python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"`.

## Schritt 1 – Gegenstände erkennen
Alle Kontaktbögen sichten; bei Unklarheit Einzelbilder öffnen. Erfasse ALLES, was zum Hausrat oder zum Gebäude gehören könnte – nichts vergessen.

Regeln:
- **Einzelposition** für jeden Gegenstand mit geschätztem Neuwert ab der Grenze (Standard **50 €**), Marke/Modell so genau wie erkennbar.
- **Sammelposten** pro Raum für Kleinkram darunter (z. B. „Kosmetik/Pflegeprodukte, ca. 45 Stück“, „Handtücher, ca. 20 Stück“) mit Anzahl × Durchschnittspreis.
- **Kleidung**: pro Schrank/Kategorie schätzen (Jacken, Hosen, Shirts, Schuhe …) als Stückzahl × typischer Markenpreis; nur klar hochwertige Einzelstücke separat.
- **Qualitätsannahme** (Standard gehobene Markenqualität, nicht Billigsegment). **Möbel nur dann als IKEA ansetzen, wenn IKEA eindeutig erkennbar ist** (typische Serie oder Ansage). Sonst Vergleich mit Markenherstellern aus dem Möbelhaus (z. B. Nolte, Staud, Rauch Select, hülsta, Musterring). Marke/Modell nicht erkennbar → Preis für gehobenes Mittelklasse-Produkt und `hinweis: "Modell unklar – bitte prüfen"`.
- **Zuordnung**: `Hausrat` (bewegliche, freistehende Sachen), `Gebäude` (fest eingebaut: Sanitärobjekte, Fliesen, Heizkörper, Dachfenster, Einbauküche/Badmöbel nach Maß, Markise …), `Unklar` (Grenzfälle, z. B. verschraubter Spiegelschrank, Serien-Badmöbel, Solarmodule). Freistehend → Hausrat, fest verbaut → Gebäude.
- **Flächen** (Fliesen, Böden) grob schätzen und `hinweis: "Fläche geschätzt – bitte prüfen"`.
- Personen im Spiegel ignorieren.
- **Stichtagsprinzip**: Erfasst wird, was **in diesem Video zu sehen ist**, auch wenn es nur vorübergehend dort liegt (abgelegte Kleidung, Wäsche, Taschen, Geräte zum Laden …). Nichts auf einen anderen Raum verschieben.
- **Nicht erfassen:** Defektes oder zur Entsorgung Bestimmtes (laut Ansage), Inhalte geschlossener Kartons (nur Pauschale, außer der Nutzer nennt den Inhalt), Müll, Mietgeräte des Anbieters (z. B. Router), Ersatzteile der Haustechnik, Eigentum von Nachbarn, Pflanzen.
- **Pakete:** Wurde etwas als Paket gekauft (Küche, Wärmepumpe …) und der Nutzer nennt den Paketpreis: eine Hauptposition mit dem Paketpreis, die Komponenten als Dokumentationsposten mit `einzelpreis: 0` und `hinweis: "im Preis von <ID> enthalten"`. Förderungen nicht abziehen.

### Quellen und Ansagen
- **Rangfolge:** Nutzer > Rechnung > Ansage im Video > eigene Bilderkennung > Schätzung.
- Nennt der Nutzer einen **Kaufpreis** (Ansage/Chat), gilt dieser als Preisquelle (`preis_quelle: "Kaufpreis laut Nutzer (Jahr)"`), keine Online-Recherche nötig.
- Das Transkript ist eine **automatische Abschrift**. Klingt ein Wort wie eine bekannte Marke und passt es zu Bild und Zusammenhang („Knurps“ → Knirps, „Sonnens“ → Sonos, „Wellenstein“ → Wellensteyn, „Jusk“ → JYSK), korrigiere selbst und vermerke es im Hinweis („Ansage t01m12s, gehört: Knurps“). Nur bei echtem Widerspruch zwischen Ansage und Bild (z. B. anderer Gerätetyp) nachfragen.

### Dubletten vs. echte Mehrfachstücke
Jede Sekunde ist ein Bild – derselbe Gegenstand taucht meist in vielen Bildern auf. Die Bögen **chronologisch als Kamerafahrt** lesen und zuerst eine grobe Raumkarte bilden (Zonen: „Waschtisch“, „Spiegelschrank 2. Fach“, „Unterschrank links“ …). Dann:
- **Gleiche Stelle = gleicher Gegenstand**, auch aus anderem Winkel oder nach einem Schwenk zurück. Maßgeblich ist der Fundort samt Umgebung, nicht das Aussehen allein.
- **Mehrfach zählen nur mit Beleg**: beide Exemplare gleichzeitig im Bild, oder eindeutig unterschiedliche Fundorte.
- **Im Zweifel** einmal zählen und `hinweis: "Anzahl prüfen – evtl. 2× (t00m45s / t01m30s)"`.
- Nur Gegenstände erfassen, die **physisch in diesem Raum** stehen – durch Türen sichtbare Dinge gehören zum Nachbarraum.
- Pro Position `fundort` und `gesehen_bei` (alle Zeitstempel) angeben – das macht die Zählung nachprüfbar.

### Dubletten über Räume hinweg
- **Türen** zählt der Raum, in den sie führen; Flure zählen keine Türen.
- **Treppen** bekommen ein eigenes Video.
- **Leere Kartons** und **Zubehör**, dessen Gerät in einem anderen Raum steht: `einzelpreis: 0` mit Verweis auf die ID.
- Gleiche Möbel in mehreren Räumen einheitlich bepreisen. Vor dem Abschluss die anderen Raumdateien nach ähnlichen Positionen durchsuchen.

**Zwischenstand sofort sichern:** Direkt nach Schritt 1 die JSON-Datei (Format siehe Schritt 4) mit allen Positionen und geschätzten Preisen schreiben (`preis_url` leer, `hinweis` ergänzt um „Preis noch nicht recherchiert“) und die Standbilder kopieren. Während Schritt 2 die Datei nach jeweils ca. 10 recherchierten Positionen aktualisieren.

## Schritt 2 – Preis recherchieren (Neuwert = heutiger Wiederbeschaffungspreis)
Für jede Einzelposition einen aktuellen Preis online suchen: gleiches Modell oder heutiges Nachfolge-/Vergleichsmodell gleicher Art und Güte (darf unter dem alten Kaufpreis liegen). Bevorzugt Herstellershop, idealo, geizhals, große Händler. Realistischen Marktpreis nehmen (nicht den absurdesten Billigstanbieter, nicht UVP-Mondpreis).
`preis_url` muss eine **konkrete Produktseite** mit sichtbarem Preis sein (keine Kategorie- oder Suchseite, keine Herstellerseite ohne Preis) – davon wird später ein Screenshot gemacht. geizhals-Produktseiten sind ideal (Preis + Datum im Bild).
Festhalten: `preis_url`, `preis_quelle` (Shop/Seite), `preis_auszug` (kurzer Textauszug mit Preis), `abrufdatum`.
Sammelposten: Schätzung reicht, Begründung in `hinweis`.
**Keine Browser-Werkzeuge benutzen** – die Screenshots macht später `tools/nachweise.py`. Preise, die eine Seite erst per JavaScript lädt, werden am Screenshot bestätigt.

## Schritt 3 – Standbild je Position
Für jede Einzelposition das beste Einzelbild wählen und nach `PROJ/Standbilder/<KÜRZEL>/<ID>.jpg` kopieren (Sammelposten: ein repräsentatives Bild).

## Schritt 4 – Ergebnis schreiben
Datei `PROJ/data/raeume/<Name>.json` (UTF-8, eingerückt; Dateiname ohne Umlaute):

```json
{
  "video": "Badezimmer_OG.MOV",
  "raum": "Badezimmer OG",
  "kuerzel": "BAD-OG",
  "verarbeitet_am": "2026-09-25",
  "positionen": [
    {
      "id": "BAD-OG-001",
      "gegenstand": "Haarstyler mit Aufsätzen und Box",
      "marke_modell": "Dyson Airwrap Complete Long",
      "kategorie": "Elektrogeräte klein",
      "zuordnung": "Hausrat",
      "anzahl": 1,
      "einzelpreis": 549.00,
      "sammelposten": false,
      "sicherheit": "hoch",
      "preis_url": "https://…",
      "preis_quelle": "dyson.de",
      "preis_auszug": "Dyson Airwrap Complete Long … 549,00 €",
      "abrufdatum": "2026-09-25",
      "standbild": "Standbilder/BAD-OG/BAD-OG-001.jpg",
      "video_zeit": "01:12",
      "fundort": "Unterschrank rechts, unteres Fach",
      "gesehen_bei": ["t01m10s", "t01m12s", "t01m33s"],
      "hinweis": ""
    }
  ]
}
```

Feldwerte:
- `kategorie` genau eine aus: Möbel · Elektronik/Unterhaltung · Computer/Büro · Haushaltsgeräte groß · Elektrogeräte klein · Küche/Geschirr · Heimtextilien · Kleidung/Schuhe · Kosmetik/Hygiene · Deko/Kunst · Bücher/Medien · Sport/Freizeit · Fahrräder · Werkzeug/Garten · Spielzeug · Schmuck/Uhren/Wertsachen · Vorräte · Sonstiges · Gebäudebestandteil
- `sicherheit`: `hoch` (Modell erkannt + Preis belegt), `mittel` (Typ klar, Modell geschätzt), `niedrig` (grobe Schätzung)
- `kuerzel`: kurz, Großbuchstaben, eindeutig pro Raum (z. B. BAD-OG, KUE-EG, WOZI-EG, GARAGE)
- IDs fortlaufend `<KÜRZEL>-001` …
- Das Feld `nachweis` setzt nur `tools/nachweise.py apply` – nie von Hand.

### Video mit mehreren Räumen oder mehreren Teilen
- Zeigt ein Video mehrere Räume (z. B. ein ganzes Stockwerk), pro Raum eine eigene Datei: `data/raeume/<Videoname>__<Raum>.json`, jeweils mit eigenem `raum`, `kuerzel` und eigener ID-Folge. Raumwechsel an Türdurchgängen erkennen; Flure/Treppen als eigener Raum. Raumnamen in der Rückmeldung nennen, damit der Nutzer sie korrigieren kann.
- Mehrteilige Videos (`Raum_1`, `Raum_2`) als **ein** Raum auswerten; in `gesehen_bei` und `video_zeit` Präfix `V1 t…` / `V2 t…`; den Übergang besonders auf Doppelzählungen prüfen.

### Erneut auswerten
Wird ein Raum nachgefilmt, die bestehende Raumdatei lesen und die IDs vorhandener Gegenstände beibehalten. Korrekturen des Nutzers (Hinweis „laut Nutzer bestätigt“, `data/korrekturen.json`) und Ausschlüsse (`data/ausgeschlossen.json`) bleiben bestehen.

## Hinweise je Raumtyp
- **Küche:** Einbauküche nach Maß → Unklar oder Gebäude; Elektrogeräte einzeln mit Typenschild; Geschirr, Besteck, Töpfe, Vorräte als Sammelposten.
- **Hauswirtschaftsraum/Keller:** Waschmaschine, Trockner, Gefriertruhe einzeln; Haustechnik (Heizung, Wärmepumpe) → Gebäude.
- **Werkstatt/Garage:** Werkzeug von Markenherstellern einzeln ab Grenze, Kleinwerkzeug als Sammelposten; Fahrräder Kategorie „Fahrräder“, E-Bikes genau erfassen.
- **Vorratsraum:** Vorräte als Sammelposten je Art.
- **Wohnzimmer:** Bilder und Medien (Bücher, Schallplatten) zählen bzw. schätzen; Kunst nach Signatur fragen.
- **Kinderzimmer:** Spielzeug als Sammelposten je Art (LEGO-Sets ggf. einzeln).
- **Garten, Gartenhaus, Schuppen:** keine Pflanzen; `hinweis: "Außenbereich – Deckung laut Tarif prüfen"` bzw. „Nebengebäude – Deckung laut Tarif prüfen“.

## Wertsachen und Sammlungen (Fotos statt Video)
- Eigene Raumdatei, z. B. `data/raeume/Wertsachen.json` mit `kuerzel: "WERT"` und `video: "(ohne Video – Fotos/Angaben)"`; `gesehen_bei` enthält die Foto-Dateinamen, die Fotos dienen als Standbilder.
- HEIC-Fotos vorher in JPG umwandeln und die EXIF-Drehung beachten (z. B. Pillow mit `pillow-heif` und `ImageOps.exif_transpose`).
- **Sammlungen zählen:** Foto in überlappende Ausschnitte teilen und Stück für Stück markieren; Anzahl mit Unsicherheit angeben („ca. 85 ± 3“). Die Zählung auf dem Foto schlägt die Schätzung des Nutzers, wird aber markiert. Sonderstücke ab Grenze einzeln, Rest als Anzahl × Durchschnittspreis; für genaue Bewertung nach Artikelnummern fragen.
- **Kunst:** Signatur im Detailfoto lesen, Galeriepreise suchen; Zertifikate nach `Belege/`.
- Mit vorhandenen Sammelposten anderer Räume abgleichen (z. B. Deko in der Werkstatt), damit nichts doppelt zählt.

## Rechnungen
Rechnungen aus `Belege/` lesen (Händler, Datum, Positionen, Beträge) und der passenden Position zuordnen: `hinweis` um „Rechnung: Belege/<Datei>, gekauft <Datum> für <Betrag>“ ergänzen, `sicherheit: "hoch"`. Der Neuwert bleibt der heutige Preis. Rechnungen ohne passenden Gegenstand mit dem Nutzer klären (nachfilmen oder Position ergänzen).

## Rückmeldung
Kurz: Anzahl Positionen, Summe Hausrat / Gebäude / Unklar, die 5 teuersten Positionen, Auffälligkeiten (unscharfe Stellen, Bereiche, die nachgefilmt werden sollten).
