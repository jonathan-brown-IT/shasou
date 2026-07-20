"""
Generates data/audio_manifest.json — real neural TTS audio (VOICEVOX) for every
phrase, vocab word, and song title used in the app, base64-encoded as opus/ogg.

Prerequisites: run scripts/setup_voicevox.sh first.

Edit PHRASES / VOCAB / SONGS below to add content, then re-run this script,
then re-run build.py to bake the new audio into dist/index.html.
"""
import subprocess, base64, json, os, sys
from voicevox_core.blocking import Onnxruntime, OpenJtalk, Synthesizer, VoiceModelFile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VV_DIR = os.path.join(ROOT, "vv")

# Style IDs available in 0.vvm — swap STYLE_ID to change the voice:
#   2 = Shikoku Metan (Normal)   3 = Zundamon (Normal)
#   8 = Kasukabe Tsumugi (Normal)  10 = Amehare Hau (Normal)
# (Metan/Zundamon/Tsumugi/Hau each also have あまあま/ツンツン/セクシー style variants
#  at other IDs — run list_styles() below to see the full set for your .vvm file.)
STYLE_ID = 2

PHRASES = [
    "これは山手線です。", "次は渋谷駅です。", "今、何時ですか。", "電車はとても速いです。",
    "外は雨が降っています。", "私は毎日、電車で学校へ行きます。", "この席は空いていますか。",
    "すみません、切符を落としました。", "新宿で乗り換えます。", "窓の外はきれいですね。",
    "今日は少し疲れました。", "駅の前にコンビニがあります。", "夜の街はにぎやかです。",
    "もうすぐ終電です。", "この電車は各駅停車です。", "明日も晴れるといいですね。",
    "駅員さんに道を聞きました。", "混んでいるので、次の電車を待ちます。",
    "この時間帯はいつも人が多いです。", "雨の日は電車が遅れやすいです。",
    "今度、一緒に東京を回りましょう。", "目を閉じると、少し眠くなります。",
    "この曲、電車に合いますね。", "一日の終わりに、この景色を見るのが好きです。",
    "次で降りますので、通してください。",
    "今日は天気がいいですね。", "雪が降ってきました。", "曇っていて、少し寒いです。",
    "電車の中で音楽を聞きます。", "週末はどこへ行きますか。", "友達と原宿で買い物をしました。",
    "この本は駅の売店で買いました。", "次の電車まで十分待ちます。", "座席を譲ってくれてありがとう。",
    "今朝は寝坊してしまいました。", "スマホの充電が切れそうです。", "明日は早く起きなければなりません。",
    "秋の空気は気持ちがいいです。", "桜の季節はとても人気があります。", "このアプリで乗り換え案内を調べます。",
    "台風のせいで電車が止まりました。", "傘を持ってくればよかったです。", "東京の夜景はとてもきれいです。",
    "私は窓側の席が好きです。", "隣の人がずっと寝ています。", "今度の連休はどこか行きますか。",
    "このホームは意外と静かです。", "電車が満員で乗れませんでした。", "時刻表を確認してください。",
    "一駅分歩くことにしました。",
]
VOCAB = [
    "駅", "窓", "雨", "疲れる", "混む", "景色", "乗り換える", "終電",
    "天気", "傘", "晴れ", "曇り", "雪", "台風", "満員", "時刻表",
    "売店", "寝坊", "充電", "座席", "夜景", "連休", "静か",
]
SONGS = [
    "プラスティック・ラブ", "ライド・オン・タイム", "金曜日の夜", "シティ・コネクション",
    "渚のバルコニー", "ボイジャー", "真夜中のドア", "言い出せなくて", "元気を出して", "あの日にかえりたい",
]


def list_styles(synth):
    for m in synth.metas():
        print(m.name, [(s.name, s.id) for s in m.styles])


def main():
    ort_lib_candidates = [
        f for f in os.listdir(os.path.join(VV_DIR, next(
            d for d in os.listdir(VV_DIR) if d.startswith("voicevox_onnxruntime")
        ), "lib"))
        if f.startswith("libvoicevox_onnxruntime.so.")
    ]
    ort_dir = next(d for d in os.listdir(VV_DIR) if d.startswith("voicevox_onnxruntime"))
    ort_lib = os.path.join(VV_DIR, ort_dir, "lib", sorted(ort_lib_candidates)[-1])

    ort = Onnxruntime.load_once(filename=ort_lib)
    jtalk = OpenJtalk(os.path.join(VV_DIR, "open_jtalk_dic_utf_8-1.11"))
    synth = Synthesizer(ort, jtalk)
    vvm = VoiceModelFile.open(os.path.join(VV_DIR, "models", "0.vvm"))
    synth.load_voice_model(vvm)

    if "--list-styles" in sys.argv:
        list_styles(synth)
        return

    tmp_dir = os.path.join(ROOT, "_audio_tmp")
    os.makedirs(tmp_dir, exist_ok=True)

    manifest = {}
    all_items = PHRASES + VOCAB + SONGS
    for i, text in enumerate(all_items):
        wav_bytes = synth.tts(text, style_id=STYLE_ID)
        wav_path = os.path.join(tmp_dir, f"{i}.wav")
        ogg_path = os.path.join(tmp_dir, f"{i}.ogg")
        with open(wav_path, "wb") as f:
            f.write(wav_bytes)
        subprocess.run(
            ["ffmpeg", "-y", "-i", wav_path, "-c:a", "libopus", "-b:a", "28k",
             "-ac", "1", "-ar", "24000", ogg_path],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        with open(ogg_path, "rb") as f:
            manifest[text] = base64.b64encode(f.read()).decode("ascii")
        os.remove(wav_path)
        os.remove(ogg_path)
        print(f"  [{i+1}/{len(all_items)}] {text}")

    os.rmdir(tmp_dir)
    out_path = os.path.join(ROOT, "data", "audio_manifest.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    print(f"\nWrote {len(manifest)} items to {out_path}")


if __name__ == "__main__":
    main()
