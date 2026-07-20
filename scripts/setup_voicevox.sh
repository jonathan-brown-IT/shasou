#!/usr/bin/env bash
# Downloads everything needed to run VOICEVOX CORE locally for audio generation:
#   - the Open JTalk dictionary (mirrored on GitHub, since the original SourceForge
#     host works fine for normal use but was unreachable from a restricted sandbox)
#   - the VOICEVOX ONNX Runtime build
#   - one voice model file (0.vvm — includes Shikoku Metan, Zundamon, Kasukabe Tsumugi,
#     Amehare Hau)
#
# Usage: bash scripts/setup_voicevox.sh
# Result: everything lands in ./vv/ (gitignored — don't commit these, they're large)

set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p vv/models
echo "==> Downloading Open JTalk dictionary..."
curl -sL "https://github.com/r9y9/open_jtalk/releases/download/v1.11.1/open_jtalk_dic_utf_8-1.11.tar.gz" -o vv/dict.tar.gz
tar xzf vv/dict.tar.gz -C vv/
rm vv/dict.tar.gz

echo "==> Downloading VOICEVOX ONNX Runtime..."
curl -sL "https://github.com/VOICEVOX/onnxruntime-builder/releases/download/voicevox_onnxruntime-1.23.2/voicevox_onnxruntime-linux-x64-1.23.2.tgz" -o vv/ort.tgz
tar xzf vv/ort.tgz -C vv/
rm vv/ort.tgz

echo "==> Downloading voice model (0.vvm)..."
curl -sL "https://github.com/VOICEVOX/voicevox_vvm/releases/download/0.16.4/0.vvm" -o vv/models/0.vvm

echo "==> Installing Python bindings..."
pip install "https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.4/voicevox_core-0.16.4-cp310-abi3-manylinux_2_34_x86_64.whl"

echo "Done. Run: python3 scripts/generate_audio.py"
