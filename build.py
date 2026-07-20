"""
Bakes data/audio_manifest.json into src/template.html to produce dist/index.html.

Run this after editing src/template.html and/or regenerating audio via
scripts/generate_audio.py.

Usage: python3 build.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data", "audio_manifest.json"), encoding="utf-8") as f:
    audio_json = f.read()

with open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8") as f:
    template = f.read()

PLACEHOLDER = "/*__AUDIO_DATA__*/{}/*__END_AUDIO_DATA__*/"
if PLACEHOLDER not in template:
    raise SystemExit(
        "Couldn't find the audio data placeholder in src/template.html — "
        "make sure it still contains: " + PLACEHOLDER
    )

output = template.replace(PLACEHOLDER, audio_json)

out_path = os.path.join(ROOT, "dist", "index.html")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(output)

print(f"Built {out_path} ({len(output):,} bytes)")
