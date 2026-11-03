---
name: remo-5
description: Produksi video explainer 2.5D bergaya "bongkar benda" vertikal 9:16 — rig SVG cel-shaded berlapis, single state controller, HUD telemetri, callout, dan kartu diagram — untuk menjelaskan cara kerja satu benda sehari-hari. Kalau user memanggil /remo 5 dan menyebut satu benda, langsung bangun prototipe benda itu tanpa VO, kecuali user mengirim file VO.
---

# REMO 5

VIDEO EXPLAINER 2.5D — BONGKAR BENDA

REMO 5 adalah skill terpisah dari REMO 4, dan REMO 4 tetap berjalan
dengan standarnya sendiri. Jangan mencampur aturan keduanya, jangan
mengedit skill atau template REMO 4 untuk keperluan REMO 5, dan jangan
mengubah skill ini menjadi REMO 4 versi lain.

Perbedaan intinya:

- REMO 4: dynamic visual storytelling per topik — riset, naskah,
  karakter, identitas visual yang berubah mengikuti cerita.
- REMO 5: satu benda, satu mekanisme, satu variabel utama. Visualnya
  selalu rig SVG 2.5D di atas meja kerja, bukan karakter, bukan
  slideshow foto, dan bukan mesh 3D.

Skill ini lahir dari dua bukti, bukan dari klaim:

1. Video referensi "Kita Bongkar - Gunting" (Animantra, 92 detik)
   dianalisis sebagai 2.5D vector rig, bukan Three.js: kamera hanya
   zoom/pan 2D, "tampak samping" adalah kartu diagram, bayangan adalah
   duplikat siluet, dan exploded view adalah layer terpisah. Catatan
   jujur: dari video saja tidak bisa dibuktikan engine persisnya
   (Remo-4, Remotion, After Effects shape layer, dan sejenisnya bisa
   menghasilkan tampilan yang sama). Yang ditiru REMO 5 adalah
   arsitekturnya, bukan nama enginenya.
2. Prototipe referensi: hekter / stapler, 2026-11-03, folder
   `~/workspace/kita-bongkar-stapler/` (stapler-final.mp4, 1080x1920,
   30 fps, 24 detik, 6,7 MB, tanpa VO). User menilainya dengan reaksi
   ❤️ dan kalimat "keren bro konsepnya bagus". Pola di prototipe itu
   adalah pola yang dipakai ulang di sini.

## 1. CARA PANGGIL (mengikat)

- User memanggil `/remo 5` dan menyebut satu benda → langsung bangun
  prototipe benda itu. Jangan minta persetujuan tiap tahap, jangan
  berhenti di riset panjang, jangan menunggu naskah.
- Default: TANPA VO. Teks di layar diatur langsung oleh `render(t)`
  di `animatic.html`, bukan dari `words.js`.
- Kalau user mengirim file VO (WAV atau MP3): simpan apa adanya,
  jangan konversi diam-diam. Durasi video mengikuti durasi VO aktual.
  JANGAN percepat/perlambat VO untuk memaksa durasi tertentu, kecuali
  user minta eksplisit. Tiap produksi wajib `words.js` baru dari
  transkripsi aktual audio itu, atau dari estimasi yang dilabeli
  ESTIMASI di mana pun ia dipakai. Jangan pernah pakai `words.js`
  proyek sebelumnya, dan jangan klaim estimasi sebagai transkripsi.
- REMO 5 default TANPA presenter/avatar. Jangan memaksakan karakter
  di setiap adegan. Kalau user minta presenter, gender avatar HARUS
  cocok dengan gender VO (VO cewek → tokoh cewek, VO cowok → tokoh
  cowok); kalau gender VO tidak jelas, TANYAKAN dulu, jangan menebak.
  Ini pelajaran dari video medan magnet REMO 4 yang harus di-render
  ulang jadi v2 karena avatar tidak cocok.
- LOKAL SAJA. Skill ini tinggal di `~/workspace/custom-skills/remo-5/`
  dan proyeknya di `~/workspace/kita-bongkar-<benda>/`. JANGAN push ke
  GitHub, jangan buat repo baru, jangan publikasikan, sampai user
  minta eksplisit. Workspace ini sendiri bukan repo git — jangan
  menginisialisasi repo hanya untuk skill ini.

## 2. PRINSIP OPERASI

- Kerjakan di VM/runtime Muse, bukan menyuruh user menjalankan
  perintah di komputer lokal.
- MP4 final adalah deliverable wajib kalau runtime mendukungnya.
  Jangan mengakhiri pekerjaan hanya dengan naskah, kode HTML, atau
  preview, kalau rendering sebenarnya bisa dilakukan.
- Jangan mengaku sudah riset, render, atau menghasilkan file kalau
  belum benar-benar berhasil dan terverifikasi.
- Jangan mengubah template di folder skill ini secara langsung.
  Untuk tiap benda baru: salin `template/` skill ini ke folder proyek
  baru, lalu edit salinan itu.
- Jangan mengedit file apa pun di `~/workspace/Remo-4/` atau di
  `~/workspace/custom-skills/remo-4/` untuk keperluan REMO 5.
- Prioritaskan menghasilkan MP4 yang sudah lolos frame check dan
  verifikasi ffprobe, bukan sekadar "sudah di-render".

## 3. ARSITEKTUR 2.5D (ini inti skillnya, bukan hiasan)

### 3.1 Panggung

- `#stage` 540x960 di `animatic.html`, di-render per frame oleh
  `render(t)`, lalu `render.py` (Playwright + Chromium) mengambil
  screenshot tiap frame dan FFmpeg menaikkan skala menjadi
  1080x1920, 30 fps. `window.BOUNDS` adalah daftar batas adegan
  dalam detik, mis. `[0,4,9,15,20,24]`.
- Latar: meja kerja cutting mat hijau dengan grid miring −18°,
  ditambah properti statis (kertas, penggaris, pensil) yang
  dimiringkan masing-masing, untuk memberi kedalaman. Jangan tempel
  foto jadi sebagai latar.
- Kamera: HANYA zoom dan pan 2D di atas bidang yang sama. Tidak ada
  orbit/pitch/yaw 3D, tidak ada kamera yang "berputar ke samping".
  Kalau butuh tampak samping, tampilkan sebagai kartu diagram,
  bukan dengan memutar objek.

### 3.2 Rig SVG berlapis

Pecah benda menjadi grup `<g>` dengan pivot yang SAMA untuk bagian
yang bergerak bersama, mis. pada hekter: lengan atas berporos di
engsel belakang, magazine, deretan isi, satu isi tunggal, kertas,
alas + landasan.

Tiap keping utama digambar 4 tumpuk, dengan urutan ini:

1. Bayangan: duplikat path digeser (mis. 14px, 18px) dengan
   fill hitam transparan, mis. `rgba(0,0,0,0.30)`.
2. Extrusion (tebal samping palsu): duplikat path digeser sedikit
   (mis. 4px, 5px) dengan warna shade gelap + outline gelap.
3. Permukaan utama + bevel: path utama dengan warna terang, ditambah
   poligon bidang miring / highlight di sisi yang relevan.
4. Outline & highlight: garis tepi luar gelap (mis. stroke
   `#1a1d20`, 2.5) + garis kilau putih tipis di tepi lengkungan.

Aturan gambar:

- Gambar bentuk benda yang BENAR (proporsi, engsel, mulut, landasan),
  bukan kotak generik yang diberi label nama benda. Kalau bentuknya
  masih generik/penyok di frame check, perbaiki dulu — itu bagian
  tersulit, bukan kodenya, dan wajar butuh iterasi.
- Jangan pakai emoji di dalam video, untuk alasan apa pun.
- Cek dulu rig/komponen yang sudah ada di proyek REMO 5 sebelumnya
  (mis. cutting mat, HUD, kartu diagram) sebelum menggambar ulang.
  Kalau ada yang cocok, pakai itu. Kalau tidak ada yang cocok, gambar
  sendiri dan simpan di folder proyek benda itu, supaya bisa dipakai
  ulang — jangan jadi file sekali pakai yang hilang.

### 3.3 Single state controller

Satu variabel utama per adegan mekanis menggerakkan SEMUA yang
terkait. Contoh hekter: sudut tekan lengan (0° → ~28°).

Variabel itu langsung mengontrol:

- Rotasi grup yang berporos (mis. `rotate(angle pivotX pivotY)`).
- Angka telemetri di HUD kanan atas (sudut, jarak, persen, jumlah).
- Posisi bagian yang bergerak (mis. posisi isi tunggal di mulut,
  dihitung dari titik mulut yang dirotasi mengelilingi pivot).
- Keadaan payoff (mis. kaki isi yang menekuk, dihitung dari variabel
  tekuk yang diturunkan dari sudut yang sama).

Tidak ada animasi adegan mekanis yang jalan sendiri tanpa kaitan
dengan variabel ini. Kalau satu angka di HUD tidak bisa dijelaskan
asalnya dari variabel utama, angka itu salah.

Hati-hati dengan tanda dan titik putar di SVG, pelajaran dari
prototipe hekter: vektor ke bawah yang dirotasi positif bergerak ke
arah berlawanan dari dugaan, dan titik putar kaki di kartu diagram
harus dalam koordinat SVG penuh kartu itu (mis. 199/233, bukan
koordinat lokal grup). Jangan menebak tanda/koordinat — periksa di
frame check sampai kaki menekuk KE DALAM, bukan mengembang ke luar.

### 3.4 HUD, callout, dan kartu diagram

- HUD kiri atas: judul seri + label babak, mis. `BONGKAR: HEKTER`
  dan `BABAK 2 · ISI`. HUD kanan atas: angka telemetri live + label
  satuannya, mis. `22 mm / JARAK LEDAK` atau `50% / KAKI TERTEKUK`.
- Callout pin: garis SVG dari titik benda ke badge. Ujung garis
  dikunci ke koordinat lokal benda (ikut bergerak saat kamera
  zoom/pan), ujung lain menempel ke badge. Badge muncul sekali,
  lalu diam — bukan berkedip atau berpindah-pindah.
- Kartu diagram mengambang: kartu putih di paruh bawah layar untuk
  menjelaskan mekanisme mikro yang tidak terlihat dari tampak utama,
  mis. `TAMPAK SAMPING LANDASAN` dengan diagram kaki yang menekuk.
  Kartu muncul dengan transisi halus, diam selama penjelasannya,
  lalu hilang sebelum adegan berikutnya.

## 4. MEMILIH BENDA

Benda yang cocok untuk REMO 5 memenuhi semua ini:

1. Benda sehari-hari yang penontonnya langsung kenal bentuknya.
2. Mekanismenya bisa diringkas menjadi SATU variabel utama
   (sudut tekan, posisi slider, putaran kunci, jarak ledak).
3. Bagian-bagiannya terlihat dan bisa dipecah menjadi layer
   (bukan mekanisme yang seluruhnya tersembunyi di dalam kotak).
4. Ada payoff yang memuaskan di akhir: terpotong, terkunci,
   tertekuk, tersambung, terbuka.

Contoh yang sudah terbukti: hekter. Contoh yang sejalan dengan pola
ini (pilih salah satu kalau user tidak menyebut benda): resleting
(slider mengunci gigi), pulpen klik (tombol → ujung keluar),
gembok (kunci memutar → sangkutan terangkat). Jangan memaksakan benda
yang mekanismenya tidak bisa divisualkan dengan satu variabel —
lebih baik bilang tidak cocok dan usulkan benda lain, daripada
memaksakan animasi yang menyesatkan.

## 5. ALUR PRODUKSI

### Langkah 0 — Siapkan proyek

Salin `template/` skill ini ke `~/workspace/kita-bongkar-<benda>/`.
Di dalam folder proyek itu harus ada, sebelum render penuh:

- `animatic.html` (salinan yang diedit untuk benda itu)
- `render.py` dan `frames.py` (disalin dari template)
- folder `cek/` untuk frame check

Periksa runtime sebelum produksi: Python 3.10+, Node.js 18+,
FFmpeg, Chromium, Playwright. Playwright di VM ini pernah jalan
dari venv lama `~/workspace/coba-threejs-romawi/.venv/bin/python`
(Chromium sudah ter-cache di `~/.cache/ms-playwright/`). Kalau venv
itu tidak ada, buat venv baru di folder proyek dan instal
playwright di situ — jangan menginstal ke Python sistem kalau
sistem melarangnya (PEP 668), dan jangan mengklaim instalasi berhasil
kalau belum dites import-nya.

### Langkah 1 — Tentukan mekanisme dalam satu kalimat

Tulis dulu, sebelum menggambar: benda apa, variabel utamanya apa,
bagian apa yang bergerak, dan payoff-nya apa. Contoh hekter:
"satu tekan lengan (0°→28°) mendorong satu staple keluar dari mulut,
kakinya menabrak landasan lalu menekuk ke dalam, kertas terkunci."

Kalau satu kalimat itu tidak bisa ditulis, bendanya belum siap
dibangun — perjelas dulu, jangan langsung menggambar.

### Langkah 2 — Gambar rig, lalu timeline babak

Pola timeline yang dipakai prototipe hekter, dan boleh diadaptasi
durasi maupun jumlah babaknya mengikuti benda itu:

- Intro: benda utuh di mat, zoom pelan, label + callout bagian utama.
- Babak 1 — Mekanisme utama: variabel utama bergerak pelan,
  telemetri live, titik tumpu/pivot ditandai.
- Babak 2 — Isi / exploded view: bagian terpisah pelan, deretan
  komponen terlihat, satu komponen bergerak ke titik kerjanya.
- Babak 3 — Payoff: komponen menembus/menabrak/mengunci, ditunjukkan
  juga di kartu diagram tampak samping kalau tampilan utama terlalu
  kecil untuk membaca payoff-nya.
- Penutup: kembali ke benda utuh, hasil akhirnya terlihat, teks
  penutup satu baris yang merangkum rumusnya, mis.
  `TUAS + LANDASAN = TERKUNCI`.

Durasi mengikuti benda dan narasi/VO-nya, bukan dipaksa ke angka
tertentu. Prototipe hekter tanpa VO: 24 detik. Jangan memaksa
45–60 detik hanya karena itu target REMO 4 — itu standar REMO 4,
bukan REMO 5.

### Langkah 3 — Frame check (WAJIB, sebelum render penuh)

Jalankan `frames.py` di titik kunci: satu frame per babak + titik
transisi (mis. detik 2, 6, 11, 16, 19, 21, 23 untuk video 24 detik).
Simpan JPG-nya di folder `cek/` proyek dan LIHAT gambarnya secara
langsung. Jangan lanjut render penuh hanya bermodal log program.

Checklist frame check:

- Bentuk benda benar, tidak generik, tidak penyok.
- Tidak ada teks terpotong, badge terpotong tepi, atau kartu
  terpotong kiri-kanan. Kalau ada, geser badge/kartu ke dalam dan
  turunkan skala kamera — pada hekter, skala maks diturunkan dari
  1,25x menjadi 1,14x untuk menyelesaikan ini.
- Tidak ada elemen bertumpuk yang seharusnya terpisah (mis. deret
  isi menumpuk magazine — pada hekter diperbaiki dengan menaikkan
  jalur isi ke celah antara lengan dan magazine).
- Urutan waktu benar: penutup tidak boleh muncul saat bagian masih
  terbuka (pada hekter, lengan dikembalikan ke 0° dulu, isi final
  muncul, baru teks penutup penuh).
- Arah gerakan benar: kaki/diagram menekuk KE DALAM, bukan ke luar.
- Informasi terbaca di layar HP: subtitle/label cukup besar,
  kontras cukup, tidak ada elemen yang menutupi informasi penting.

Perbaiki `animatic.html`, ulangi frame check, sampai lolos. Jangan
melanjutkan render penuh kalau ada kesalahan visual yang signifikan.

### Langkah 4 — Render penuh dan audio

Jalankan `NAME=<benda> python render.py` (tambah argumen file audio
kalau ada VO, sesuai perilaku `render.py` di template). Render
menghasilkan MP4 1080x1920, 30 fps.

Audio:

- Tanpa VO: musik latar pelan SELALU dipakai — ambien lembut,
  fade in/out, volume jelas di bawah (tidak ada narasi yang harus
  dikalahkan, tapi musik tetap tidak boleh mendominasi). Pada
  prototipe hekter, audio yang dipakai adalah ambien sintetis pelan
  buatan FFmpeg, dan itu HARUS disebut sebagai ambien sintetis,
  bukan diklaim sebagai musik rekaman.
- Suara transisi JANGAN keras/kasar — tanpa slam, ledakan, atau
  efek nendang. Pakai whoosh/pop lembut dengan volume diturunkan,
  atau tanpa SFX tambahan sama sekali kalau ambien saja sudah cukup
  untuk tes itu. Jangan mengada-adakan SFX yang tidak ada di file.
- Dengan VO: narasi tetap dominan, musik di bawah narasi, SFX
  lembut seperti di atas.

### Langkah 5 — Verifikasi final dan delivery

Setelah render, verifikasi SEBELUM mengklaim selesai:

- File benar-benar ada, ukuran > 0.
- `ffprobe`: resolusi 1080x1920, 30 fps, durasi sesuai BOUNDS.
- Ekstrak dan LIHAT frame awal, tengah, dan akhir dari MP4 final:
  tidak hitam, tidak rusak, label dan diagram terbaca.
- Audio tersedia, tidak rusak, tidak ada suara keras yang tidak
  direncanakan.

Kalau render gagal, laporkan tahap yang gagal, error sebenarnya,
file yang berhasil dibuat, dan file yang belum berhasil dibuat.
Jangan mengklaim MP4 final tersedia kalau file itu tidak benar-benar
bisa diakses user.

Serahkan MP4 sebagai attachment di chat yang sama, beserta:

- Durasi, resolusi, fps, dan ukuran dari ffprobe (angka aktual,
  bukan perkiraan).
- Babak dan mekanisme yang ditunjukkan.
- Audio yang dipakai, dengan jujur (rekaman / sintetis / tanpa SFX).
- Batasan yang masih ada, mis. pada hekter: kertas yang dijepit
  tipis dan aksi tekuk paling jelas lewat kartu diagram — kalau
  dijadikan video final, bagian yang paling layak diperbesar adalah
  zoom khusus ke mulut benda di babak payoff.
- Pertanyaan penutup yang spesifik: bagian mana yang mau diperbaiki,
  atau benda berikutnya apa.

## 6. GERAKAN TENANG (aturan dari trial hybrid, berlaku di sini)

- Zoom pelan, skala maks 1,35x. Prototipe hekter memakai maks 1,14x
  dan itu sudah cukup — jangan menaikkan skala hanya demi dramatis.
- Popup/callout/badge muncul sekali, lalu diam. Tidak ada gerakan
  pindah-pindah tiap detik yang membuat mata capek.
- Transisi lebih lama, hold lebih lama. Kalau satu adegan terasa
  "puyeng" saat ditonton, itu cacat, bukan gaya — turunkan jumlah
  dan kecepatan gerakannya sebelum render penuh.

## 7. BATASAN YANG TETAP BERLAKU

- Jangan memakai nama, logo, atau aset milik kreator referensi
  (mis. Animantra). Judul di video memakai judul sendiri, mis.
  `BONGKAR: HEKTER`, bukan judul seri milik orang lain.
- Jangan mengklaim video ini Three.js, dan jangan mengklaim
  engine referensi sudah terbukti dari video — yang terbukti hanya
  arsitektur 2.5D-nya.
- Jangan mengklaim fakta teknis (ukuran, gaya, material) di narasi
  atau kartu tanpa verifikasi. Kalau angkanya adalah angka
  ilustrasi dari animasi (mis. jarak ledak di HUD), pastikan ia
  konsisten dengan gerakan yang ditampilkan, dan jangan disajikan
  sebagai spesifikasi resmi produk.
- Video generatif tidak tersedia untuk akun/region ini — jalurnya
  tetap animasi kode + rakitan FFmpeg, sama seperti REMO 4.
- Jangan mencampur gaya karakter 3D dan SVG dalam satu adegan tanpa
  penyesuaian gaya, kalau suatu saat presenter ditambahkan.

## 8. REFERENSI PROYEK

- Prototipe pertama: `~/workspace/kita-bongkar-stapler/`
  (`animatic.html`, `render.py`, `frames.py`, `cek/`,
  `stapler-final.mp4`). Baca file ini kalau butuh contoh nyata
  pola HUD, callout, kartu diagram, dan single state controller —
  jangan menyalinnya mentah-mentah untuk benda lain tanpa
  menggambar ulang rig benda itu.
- Template starter skill ini: `~/workspace/custom-skills/remo-5/template/`
  (`animatic.html` kerangka, `render.py`, `frames.py`). Template
  ini adalah titik awal, bukan hasil jadi — rig benda selalu
  digambar per proyek.

---

Catatan penggunaan untuk Manggala: skill ini adalah REMO 5, dibuat
2026-11-03 atas permintaan Manggala, lokal saja, tanpa push GitHub.
REMO 4 tetap dengan standarnya dan tidak diubah oleh skill ini.
Kalau Manggala memanggil `/remo 5` dan menyebut satu benda, langsung
bangun prototipe benda itu (default tanpa VO). Kalau Manggala
mengirim VO, ikuti aturan VO di bagian 1.
