# densha-fork

An ambient Japanese-study train ride — a personal fork/reinterpretation of
[jivx.com/densha](https://jivx.com/densha). Rides a real Yamanote Line loop
(all 30 actual stations, LED departure-board style), drops N5/N4-level
phrases and city-pop song titles into a subtitle overlay with real
pronunciation audio, and plays a generated lofi bed underneath.

**[Open `dist/index.html`](./dist/index.html) — that's the whole app, no server needed.**

## Features

- Real Yamanote Line loop with a live JST clock, date, and time-of-day sky
- Live Tokyo weather next to the date (temperature + icon — sun/cloud/rain/snow/storm/fog),
  via [Open-Meteo](https://open-meteo.com/) (free, no API key, fetched client-side)
- ~49 N5/N4-level phrases and 39 vocab words for quiz mode (growing — see below)
- Rain/snow visual FX on the train window — Auto (follows real Tokyo weather),
  forced on, or off
- Adjustable subtitle text size (S/M/L)
- Music mood: Lofi (default) or Rainy Night (slower, wetter, adds rain ambience)
- Adjustable ride speed (compresses the real ~65 min loop)
- Frequency dial for how often text appears: Off / Rare / Frequent
- Content toggle: phrases / song titles / both
- Quiz check-ins (multiple-choice vocab recall)
- Real neural TTS pronunciation audio for every phrase, word, and title
  (via [VOICEVOX](https://voicevox.hiroshiba.jp/) — see Credits below)
- Auto-play audio toggle
- Generated lofi ambience (Tone.js — soft e-piano stabs, boom-bap drums,
  a sparse pentatonic "koto" motif; not a licensed track, so no rights issues)
- Star/save phrases, export as tab-separated text for Anki import
- Settings + saved list persist across visits (Claude artifact storage API —
  if you move this off Claude, swap `window.storage` calls for `localStorage`)

## Repo layout

```
src/template.html      – the actual app source (HTML/CSS/JS). Edit this.
data/audio_manifest.json – generated TTS audio, keyed by Japanese text, base64 opus
scripts/setup_voicevox.sh – downloads the VOICEVOX runtime/dict/voice model
scripts/generate_audio.py – (re)generates data/audio_manifest.json
build.py                – bakes the manifest into src/template.html → dist/index.html
dist/index.html          – the built, shippable file (this is what you open)
```

## Adding more content (phrases / vocab / songs)

1. Edit the `PHRASES` / `VOCAB` / `SONGS` lists in `scripts/generate_audio.py`
   **and** the matching arrays in `src/template.html` (`phrases`, `vocab`, `songs`)
   — keep the Japanese text identical in both places, since the audio manifest
   is keyed by exact text match.
2. First time only: `bash scripts/setup_voicevox.sh` (downloads ~90MB of
   runtime/dictionary/voice model into `./vv/`, gitignored).
3. `python3 scripts/generate_audio.py`
4. `python3 build.py`
5. Open `dist/index.html` to check it, commit, push.

Changing the voice: `scripts/generate_audio.py` has a `STYLE_ID` constant.
Run `python3 scripts/generate_audio.py --list-styles` after setup to see the
character/style IDs available in the bundled voice model (Shikoku Metan,
Zundamon, Kasukabe Tsumugi, Amehare Hau, each with a few style variants).

## Other ideas to build on

- More Yamanote-adjacent lines (Chuo, Keihin-Tohoku) as alternate routes
- N3+ content tier once N5/N4 feels too easy
- A real spaced-repetition scheduler instead of random draw from the pool
- Swap `window.storage` for a backend if you want stats across devices
- A proper 3D/voxel skyline (Three.js) instead of the current flat parallax blocks

## Credits & licensing

- **Voice**: synthesized with [VOICEVOX](https://voicevox.hiroshiba.jp/),
  character **Shikoku Metan** (四国めたん). VOICEVOX voices are free to use
  in projects like this, but their terms ask that you credit the character
  when you use their voice — keep the credit line already in the app (bottom
  of the control panel), and see VOICEVOX's site for the full terms if you
  publish this somewhere.
- **Music**: fully generated in-browser with [Tone.js](https://tonejs.github.io/) —
  not a licensed recording, so no attribution/rights issue there.
- **Everything else** (code, phrases, station data, design): MIT, see `LICENSE`.
  Station names/order reflect the real JR Yamanote Line; segment timings are
  approximate, not an official timetable.
