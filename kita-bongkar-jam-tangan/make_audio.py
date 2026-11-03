#!/usr/bin/env python3
"""Audio pendukung SINTETIS untuk jam-tangan-final-sfx.mp4 (bukan rekaman):
- mix.wav = ambien pad lembut + detak tik-tok lembut.
- Detak mengikuti state controller yang SAMA dengan video:
  normal 2 detak/detik; adegan 5 (34-37.5 dtk) detak makin cepat
  (lari liar), 37.5-40 dtk diam (beku), 40-46 dtk kembali 2 detak/detik.
- VO tetap dominan: ambien RMS ~-30 dBFS, detak peak ~-22 dBFS,
  sementara VO mean -16.1 dB / max -1.2 dB.
"""
import wave
import numpy as np

SR = 48000
DUR = 46.0
N = int(SR * DUR)
t = np.arange(N) / SR

# --- ambien: pad A mayor lembut, LFO pelan, fade in/out ---
freqs = [110.0, 164.81, 220.0, 277.18]
amps = [0.045, 0.030, 0.026, 0.016]
amb = np.zeros(N)
for f, a in zip(freqs, amps):
    amb += a * np.sin(2 * np.pi * f * t) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.05 * t + f))
fade_in = np.minimum(1.0, t / 1.5)
fade_out = np.minimum(1.0, (DUR - t) / 2.0)
amb *= fade_in * fade_out

# --- detak: burst sinus teredam, selang-seling tik (2400 Hz) / tok (1800 Hz) ---
tick = np.zeros(N)
times = []
tt = 0.0
k = 0
while tt < DUR:
    times.append(tt)
    if tt < 34.0 or tt >= 40.0:
        step = 0.5
    elif tt < 37.5:
        step = 0.5 - (tt - 34.0) / 3.5 * 0.38  # 0.5 -> 0.12 dtk (lari liar)
    else:
        tt = 40.0
        continue
    tt += step
    k += 1
for i, t0 in enumerate(times):
    f = 2400.0 if i % 2 == 0 else 1800.0
    n0 = int(t0 * SR)
    ln = int(0.035 * SR)
    seg = np.arange(ln) / SR
    burst = 0.22 * np.sin(2 * np.pi * f * seg) * np.exp(-seg * 220.0)
    tick[n0:n0 + ln] += burst
    # selama adegan 5 detak sedikit lebih pelan (tidak mendominasi narasi)
    if 34.0 <= t0 < 37.5:
        tick[n0:n0 + ln] *= 0.6

mix = amb + tick
peak = float(np.max(np.abs(mix)))
rms = float(np.sqrt(np.mean(mix ** 2)))
print(f"detak: {len(times)} kali, pertama {times[0]:.2f} dtk, terakhir {times[-1]:.2f} dtk")
print(f"mix peak {peak:.3f} ({20*np.log10(peak):.1f} dBFS), RMS {rms:.4f} ({20*np.log10(rms):.1f} dBFS)")
pcm = np.clip(mix, -0.95, 0.95)
pcm16 = (pcm * 32767).astype(np.int16)
with wave.open("mix.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SR)
    wf.writeframes(pcm16.tobytes())
print("mix.wav ditulis (SINTETIS: ambien pad + detak tik-tok)")
