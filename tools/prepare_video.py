#!/usr/bin/env python3
"""Bereitet ein Raumvideo für die Inventur vor.

- zerlegt das Video mit ffmpeg und behält pro Sekunde das schärfste von 3 Bildern
  (verwackelte Schwenks fliegen raus)
- baut Kontaktbögen (3x2 Bilder mit Zeitstempel) zum schnellen Sichten
- transkribiert die Ansagen lokal mit faster-whisper (VAD gegen Halluzinationen bei Stille)

Aufruf:  python tools/prepare_video.py <Projektordner>/Videos/Kueche_EG.MOV [--sprache de] [--ohne-transkript]
Ausgabe: <Projektordner>/.work/<Videoname>/{frames,sheets,transcript.txt}

Beim ersten Transkript lädt faster-whisper das Sprachmodell (large-v3-turbo, ca. 1,6 GB).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageStat

SAMPLE_FPS = 3
FRAME_WIDTH = 720
SHEET_COLS, SHEET_ROWS, TILE_W = 3, 2, 480
HALLUZINATIONEN = {"amen", "untertitel", "vielen dank", "untertitel im auftrag des zdf",
                   "untertitel der amara.org-community", "thank you", "thanks for watching"}


def ffmpeg() -> str:
    pfad = shutil.which("ffmpeg")
    if pfad:
        return pfad
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("ffmpeg nicht gefunden. Lösung: pip install -r requirements.txt")


def run_ffmpeg(*args):
    erg = subprocess.run([ffmpeg(), "-v", "error", "-y", *args], capture_output=True, text=True)
    if erg.returncode:
        sys.exit(f"ffmpeg-Fehler: {erg.stderr.strip()[-400:]}\nIst die Videodatei vollständig kopiert?")


def arbeitsordner(video: Path) -> Path:
    projekt = video.parent.parent if video.parent.name == "Videos" else video.parent
    return projekt / ".work" / video.stem


def sharpness(img: Image.Image) -> float:
    grau = img.convert("L")
    grau.thumbnail((480, 480))
    return ImageStat.Stat(grau.filter(ImageFilter.FIND_EDGES)).var[0]


def extract_frames(video: Path, work: Path) -> list[Path]:
    raw, frames = work / "raw", work / "frames"
    for d in (raw, frames):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
    print("Video wird in Einzelbilder zerlegt …", flush=True)
    run_ffmpeg("-i", str(video), "-vf", f"fps={SAMPLE_FPS},scale={FRAME_WIDTH}:-2", "-q:v", "3", str(raw / "r_%05d.jpg"))
    raws = sorted(raw.glob("r_*.jpg"))
    sekunden = (len(raws) + SAMPLE_FPS - 1) // SAMPLE_FPS
    kept = []
    for t in range(sekunden):
        group = raws[t * SAMPLE_FPS:(t + 1) * SAMPLE_FPS]
        best = max(group, key=lambda p: sharpness(Image.open(p)))
        dst = frames / f"t{t // 60:02d}m{t % 60:02d}s.jpg"
        shutil.copy(best, dst)
        kept.append(dst)
        if (t + 1) % max(1, sekunden // 10) == 0 or t + 1 == sekunden:
            print(f"  Bild {t + 1} von {sekunden}", flush=True)
    shutil.rmtree(raw)
    return kept


def build_sheets(frames: list[Path], work: Path) -> list[Path]:
    sheets_dir = work / "sheets"
    shutil.rmtree(sheets_dir, ignore_errors=True)
    sheets_dir.mkdir()
    font = ImageFont.load_default(size=28)
    per = SHEET_COLS * SHEET_ROWS
    out = []
    for i in range(0, len(frames), per):
        chunk = frames[i:i + per]
        tiles = [Image.open(p) for p in chunk]
        tile_h = int(tiles[0].height * TILE_W / tiles[0].width)
        sheet = Image.new("RGB", (SHEET_COLS * TILE_W, SHEET_ROWS * tile_h), "black")
        draw = ImageDraw.Draw(sheet)
        for j, (p, im) in enumerate(zip(chunk, tiles)):
            x, y = (j % SHEET_COLS) * TILE_W, (j // SHEET_COLS) * tile_h
            sheet.paste(im.resize((TILE_W, tile_h)), (x, y))
            _, _, right, bottom = draw.textbbox((x + 6, y + 4), p.stem, font=font)
            draw.rectangle([x, y, right + 6, bottom + 4], fill="black")
            draw.text((x + 6, y + 4), p.stem, fill="yellow", font=font)  # z. B. t01m12s
        dst = sheets_dir / f"sheet_{i // per + 1:02d}.jpg"
        sheet.save(dst, quality=80)
        out.append(dst)
    return out


def transcribe(video: Path, work: Path, sprache: str, modell: str) -> str:
    try:
        import numpy
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper fehlt. Lösung: pip install -r requirements.txt  (oder --ohne-transkript)")
    # Ton direkt von ffmpeg als 16-kHz-Mono-Float holen (unabhängig von der Audio-Bibliothek von faster-whisper)
    erg = subprocess.run([ffmpeg(), "-v", "error", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True)
    if erg.returncode:
        sys.exit(f"ffmpeg-Fehler beim Ton: {erg.stderr.decode('utf-8', 'replace').strip()[-400:]}")
    audio = numpy.frombuffer(erg.stdout, numpy.float32)
    print(f"Ansagen werden erkannt (Modell {modell}; beim ersten Mal wird es geladen, ca. 1,6 GB) …", flush=True)
    model = WhisperModel(modell, device="cpu", compute_type="int8")
    segmente, info = model.transcribe(audio, language=sprache, vad_filter=True, condition_on_previous_text=False)
    lines, gemeldet = [], 0
    for seg in segmente:
        anteil = int(seg.end / max(info.duration, 1) * 100)
        if anteil >= gemeldet + 20:
            gemeldet = anteil - anteil % 20
            print(f"  Transkript {gemeldet} %", flush=True)
        text = seg.text.strip()
        if text and text.lower().strip(".!? ") not in HALLUZINATIONEN:
            t = int(seg.start)
            lines.append(f"[{t // 3600:02d}:{t % 3600 // 60:02d}:{t % 60:02d}] {text}")
    txt ="\n".join(lines) or "(keine Ansagen)"
    (work / "transcript.txt").write_text(txt + "\n", encoding="utf-8")
    return txt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("--sprache", default="de", help="Sprache der Ansagen (Standard: de)")
    ap.add_argument("--modell", default="large-v3-turbo", help="Whisper-Modell (Standard: large-v3-turbo)")
    ap.add_argument("--ohne-transkript", action="store_true", help="keine Spracherkennung")
    args = ap.parse_args()
    for strom in (sys.stdout, sys.stderr):
        strom.reconfigure(encoding="utf-8", errors="replace")

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")
    work = arbeitsordner(video)
    work.mkdir(parents=True, exist_ok=True)
    frames = extract_frames(video, work)
    sheets = build_sheets(frames, work)
    if args.ohne_transkript:
        txt = "(Transkript übersprungen)"
        (work / "transcript.txt").write_text(txt + "\n", encoding="utf-8")
    else:
        txt = transcribe(video, work, args.sprache, args.modell)
    print(f"Arbeitsordner: {work}")
    print(f"{len(frames)} Einzelbilder (frames/tMMmSSs.jpg), {len(sheets)} Kontaktbögen (sheets/)")
    print("Transkript:\n" + txt)


if __name__ == "__main__":
    main()
