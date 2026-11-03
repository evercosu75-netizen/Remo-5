import json, re

user_text = ("Jam tangan mekanik bisa berdetak presisi tanpa baterai, tanpa listrik, tanpa chip. "
"Di balik casing-nya, ada pegas baja yang dililit sangat rapat. Saat mengendur, pegas itu melepas energi perlahan lewat rantai roda gigi. "
"Tapi energi ini tidak boleh habis sekaligus. Di sinilah escapement bekerja, seperti gerbang mikro yang membuka dan menutup ribuan kali per jam. "
"Setiap kali gerbang terbuka, satu gigi lolos. Gerbang itu dikendalikan oleh balance wheel, roda kecil yang berayun bolak-balik di atas pegas spiral. "
"Ayunan inilah yang menentukan satu detik. Tanpa balance wheel, pegas utama akan meledak sekaligus, dan jarum jam berputar kacau lalu berhenti. "
"Jadi, yang kamu dengar bukan sekadar detak — itu suara gerbang waktu yang terus menjaga ritme.")
user_words = user_text.split()
d = json.load(open("transkrip-whisper.json"))
W = d["words"]  # 114 token whisper

# Pemetaan eksplisit (whisper memecah "bolak-balik" jadi 2 token; "—" tidak diucapkan):
# user[0..71]   <-> W[0..71]
# user[72] "bolak-balik" <-> W[72]+W[73] digabung -> [29.52, 30.16]
# user[73..104] <-> W[74..105]
# user[105] "—" <-> TIDAK ADA audio: diberi jeda 42.86-43.20 (ESTIMASI, dilabeli di bawah)
# user[106..113] <-> W[106..113]
timings, estimasi = [], []
def add(u_idx, w_start, w_end, est=False):
    timings.append([round(w_start, 2), round(w_end, 2)])
    estimasi.append(bool(est))
for i in range(0, 72):
    add(i, W[i]["start"], W[i]["end"])
add(72, W[72]["start"], W[73]["end"])                       # bolak-balik digabung
for i in range(73, 105):
    add(i, W[i + 1]["start"], W[i + 1]["end"])              # geser 1 karena gabungan
add(105, 42.86, 43.20, est=True)                            # "—" : jeda, ESTIMASI
for i in range(106, 114):
    add(i, W[i]["start"], W[i]["end"])
assert len(timings) == len(user_words) == 114
print("ESTIMASI index:", [i for i, e in enumerate(estimasi) if e], "->", user_words[105])

def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())
bad = [(i, user_words[i]) for i in range(114) if i != 105 and norm(user_words[i]) not in (norm(W[i]["word"]) if i < 72 else "")]
# cek kasar: semua kata non-dash harus cocok urut setelah pemetaan
print("timing pertama:", timings[0], "terakhir:", timings[-1])

words_js = ("// words.js — BARU, dari transkripsi AKTUAL faster-whisper (model small, bahasa id,\n"
"// word_timestamps=True) atas Jam_6_qt8r.wav (45,97 dtk), diselaraskan ke teks VO user.\n"
"// 113 dari 114 timing adalah hasil transkripsi aktual. SATU kata dilabeli ESTIMASI:\n"
"// indeks 105 (\"—\") tidak diucapkan dalam audio; timingnya [42.86, 43.20] adalah jeda\n"
"// antara kata \"detak\" dan \"itu\" — ESTIMASI, bukan transkripsi.\n"
"// Format: WORDS[i] = [mulai, selesai] dalam detik, seurut WORDTEXT[i].\n"
"var WORDTEXT = " + json.dumps(user_words, ensure_ascii=False) + ";\n"
"var WORDS = " + json.dumps(timings) + ";\n"
"var WORD_ESTIMASI = " + json.dumps([i for i, e in enumerate(estimasi) if e]) + "; // indeks kata ESTIMASI\n"
"window.WORDS = WORDS;\nwindow.WORDTEXT = WORDTEXT;\nwindow.WORD_ESTIMASI = WORD_ESTIMASI;\n")
open("words.js", "w").write(words_js)

# SRT: timing segmen whisper (aktual) + teks segmen versi user
seg_texts = [
 "Jam tangan mekanik bisa berdetak presisi tanpa baterai, tanpa listrik, tanpa chip.",
 "Di balik casing-nya, ada pegas baja yang dililit sangat rapat.",
 "Saat mengendur, pegas itu melepas energi perlahan lewat rantai roda gigi.",
 "Tapi energi ini tidak boleh habis sekaligus.",
 "Di sinilah escapement bekerja, seperti gerbang mikro yang membuka dan menutup ribuan kali per jam.",
 "Setiap kali gerbang terbuka, satu gigi lolos.",
 "Gerbang itu dikendalikan oleh balance wheel, roda kecil yang berayun bolak-balik di atas pegas spiral.",
 "Ayunan inilah yang menentukan satu detik.",
 "Tanpa balance wheel, pegas utama akan meledak sekaligus, dan jarum jam berputar kacau lalu berhenti.",
 "Jadi, yang kamu dengar bukan sekadar detak — itu suara gerbang waktu yang terus menjaga ritme.",
]
def srt_time(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
lines = []
for i, (seg, txt) in enumerate(zip(d["segments"], seg_texts), 1):
    lines += [str(i), f"{srt_time(seg['start'])} --> {srt_time(seg['end'])}", txt, ""]
open("jam-tangan.srt", "w").write("\n".join(lines))
cues = [{"start": round(s["start"],2), "end": round(s["end"],2), "text": t} for s, t in zip(d["segments"], seg_texts)]
json.dump(cues, open("cues.json","w"), ensure_ascii=False, indent=1)
print("words.js + jam-tangan.srt + cues.json ditulis ulang. cue 7:", cues[6]["text"][:60])
