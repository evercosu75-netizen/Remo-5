import json, wave
import numpy as np
from faster_whisper import WhisperModel

# Baca WAV 16kHz mono via stdlib (bypass av.decode_audio yang tidak cocok versinya)
with wave.open("/tmp/jam-16k.wav", "rb") as wf:
    assert wf.getframerate() == 16000 and wf.getnchannels() == 1
    raw = wf.readframes(wf.getnframes())
audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio, language="id", word_timestamps=True)
out = {"language": info.language, "duration": info.duration, "segments": [], "words": []}
for seg in segments:
    out["segments"].append({"start": seg.start, "end": seg.end, "text": seg.text})
    for w in seg.words:
        out["words"].append({"word": w.word, "start": w.start, "end": w.end, "prob": w.probability})
json.dump(out, open("transkrip-whisper.json", "w"), ensure_ascii=False, indent=1)
print("duration", info.duration)
print("nwords", len(out["words"]))
for w in out["words"]:
    print(f"{w['start']:6.2f}-{w['end']:6.2f}  {w['word']}")
