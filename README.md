# REMO 5 — Video Explainer 2.5D "Bongkar Benda"

Produksi video explainer vertikal 9:16 bergaya **bongkar benda**: satu benda
sehari-hari, satu mekanisme, satu variabel utama. Visualnya rig SVG 2.5D
cel-shaded berlapis di atas meja kerja — bukan karakter, bukan slideshow
foto, dan bukan mesh 3D.

Panggil dengan `/remo 5` dan sebut satu benda, langsung dibangun prototipenya.
Default **tanpa VO**; kalau dikirim file VO (WAV/MP3), durasi video mengikuti
durasi VO aktual.

## Isi repo

- `custom-skills/remo-5/SKILL.md` — skill lengkap (cara panggil, arsitektur
  2.5D, alur produksi, frame check, render, audio, batasan).
- `custom-skills/remo-5/skill.yaml` — metadata skill (`remo-5`).
- `custom-skills/remo-5/template/` — template starter: `animatic.html`
  (kerangka, ganti rig placeholder dengan rig benda yang sebenarnya),
  `render.py`, `frames.py`.
- `kita-bongkar-stapler/` — prototipe referensi: hekter (24 detik, tanpa VO).
- `kita-bongkar-jam-tangan/` — produksi pertama dengan VO: jam tangan
  mekanik (45,995 detik, 1080x1920 30fps) beserta `words.js`, SRT, dan
  skrip pembantunya.

## Cara pakai

1. Salin `custom-skills/remo-5/template/` ke folder proyek baru
   `kita-bongkar-<benda>/`.
2. Tentukan mekanisme dalam satu kalimat: benda apa, variabel utamanya apa,
   bagian apa yang bergerak, payoff-nya apa.
3. Gambar rig SVG benda itu (4 tumpuk: bayangan, extrusion, permukaan+bevel,
   outline+highlight) dan timeline babak di `animatic.html`.
4. Frame check wajib: `python3 frames.py <detik kunci>` — lihat JPG-nya,
   perbaiki sampai lolos.
5. Render: `NAME=<benda> python3 render.py [narasi.wav]` → MP4 1080x1920,
   30 fps.

Butuh Python 3.10+, Node.js 18+, FFmpeg, Chromium + Playwright.

## Catatan

- Repo ini hanya berisi file teks (skill, template, kode, SRT). File biner
  (MP4 final, VO WAV, JPG frame check) **tidak** ikut di-push dan tetap
  tersimpan lokal.
- REMO 5 terpisah dari REMO 4. Jangan mencampur aturan keduanya, dan jangan
  mengedit skill/template REMO 4 untuk keperluan REMO 5.
- Benda yang cocok: mekanismenya bisa diringkas jadi satu variabel utama
  (sudut tekan, posisi slider, putaran kunci, jarak ledak) dan ada payoff
  yang memuaskan (terpotong, terkunci, tertekuk, tersambung, terbuka).
  Contoh: hekter, resleting, pulpen klik, gembok, jam tangan mekanik.
