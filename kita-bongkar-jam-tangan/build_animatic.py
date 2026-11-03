#!/usr/bin/env python3
"""Bangun animatic.html jam tangan mekanik (REMO 5) — rig SVG 2.5D.
Satu state controller: sudut ayun balance wheel (1 Hz, 2 detak/detik).
Semua rotasi roda gigi, lolosnya gigi escape, jarum detik, dan HUD
diturunkan dari variabel itu (lihat render()).
"""
import json, math

def gear_points(r_root, r_tip, teeth, tip_frac=0.16):
    """Polygon roda gigi: gigi trapesium, pusat (0,0)."""
    pts, p = [], 2 * math.pi / teeth
    for i in range(teeth):
        a = i * p
        for frac, r in ((0.0, r_root), (0.10, r_tip), (0.10 + tip_frac, r_tip), (0.50, r_root)):
            ang = a + frac * p
            pts.append(f"{r*math.cos(ang):.1f},{r*math.sin(ang):.1f}")
    return " ".join(pts)

def escape_points(r_root, r_tip, teeth):
    """Gigi runcing escape wheel: segitiga tajam."""
    pts, p = [], 2 * math.pi / teeth
    for i in range(teeth):
        a = i * p
        for frac, r in ((0.0, r_root), (0.14, r_tip), (0.50, r_root)):
            ang = a + frac * p
            pts.append(f"{r*math.cos(ang):.1f},{r*math.sin(ang):.1f}")
    return " ".join(pts)

def spiral_path(r0, r1, turns, cx=0, cy=0, steps=140):
    pts = []
    for i in range(steps + 1):
        th = turns * 2 * math.pi * i / steps
        r = r0 + (r1 - r0) * i / steps
        pts.append(f"{cx + r*math.cos(th):.1f},{cy + r*math.sin(th):.1f}")
    return "M" + " L".join(pts)

def gear_group(gid, cx, cy, r_root, r_tip, teeth, fill, spokes=4, hub=10, escape=False):
    pts = escape_points(r_root, r_tip, teeth) if escape else gear_points(r_root, r_tip, teeth)
    sp = ""
    for k in range(spokes):
        a = k * math.pi / spokes
        x1, y1 = hub * math.cos(a), hub * math.sin(a)
        x2, y2 = (r_root - 4) * math.cos(a), (r_root - 4) * math.sin(a)
        sp += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1a1d20" stroke-width="3"/>'
    return (f'<g transform="translate({cx},{cy})"><g id="{gid}">'
            f'<polygon points="{pts}" fill="{fill}" stroke="#1a1d20" stroke-width="2.5"/>'
            f'<circle r="{r_root-6}" fill="none" stroke="#1a1d20" stroke-width="1.5" opacity="0.5"/>'
            f'{sp}<circle r="{hub}" fill="#eef2f5" stroke="#1a1d20" stroke-width="2.5"/>'
            f'<circle r="3" fill="#1a1d20"/></g></g>')

cues = json.load(open("cues.json"))
CUES_JS = json.dumps(cues, ensure_ascii=False)

html = """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<title>BONGKAR: JAM TANGAN — REMO 5</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;background:#0b1210;font-family:Arial,Helvetica,sans-serif}
  #stage{position:relative;width:540px;height:960px;overflow:hidden;background:#122019;color:#fff}
  #camera{position:absolute;inset:0;transform-origin:270px 540px}
  #sceneSvg{position:absolute;inset:0;width:540px;height:960px}
  .hud{position:absolute;top:16px;background:rgba(8,18,16,.88);border:1px solid rgba(255,255,255,.28);border-radius:12px;padding:10px 12px;z-index:10}
  #hudLeft{left:16px;max-width:300px}
  #hudLeft .brand{font-size:13px;font-weight:800;letter-spacing:1px;color:#ffcf3f}
  #hudLeft .babak{font-size:15px;font-weight:800;margin-top:2px}
  #hudRight{right:16px;text-align:right;min-width:150px}
  #hudRight .val{font-size:28px;font-weight:900;color:#ffcf3f;line-height:1}
  #hudRight .lab{font-size:11px;font-weight:700;letter-spacing:1px;margin-top:4px;color:#d7dee4}
  .badge{position:absolute;background:rgba(255,255,255,.96);color:#122019;padding:7px 11px;border-radius:11px;font-size:13px;font-weight:800;border:2px solid #1a1d20;box-shadow:0 4px 0 rgba(0,0,0,.35);z-index:5;white-space:nowrap}
  .badge small{display:block;font-size:10px;font-weight:700;color:#5a666e;letter-spacing:.5px}
  #titleBig{position:absolute;left:40px;top:104px;width:460px;text-align:center;z-index:6}
  #titleBig h1{margin:0;font-size:36px;letter-spacing:1px;text-shadow:0 3px 0 rgba(0,0,0,.45)}
  #titleBig p{margin:6px 0 0;font-size:15px;font-weight:700;color:#d7dee4;text-shadow:0 2px 0 rgba(0,0,0,.4)}
  #diagramCard{position:absolute;left:60px;top:686px;width:420px;background:rgba(255,255,255,.97);color:#122019;border:3px solid #1a1d20;border-radius:16px;padding:12px 14px;z-index:6}
  #diagramCard h3{margin:0 0 4px;font-size:15px;letter-spacing:.5px}
  #diagramCard p{margin:4px 0 0;font-size:13px;line-height:1.45;font-weight:600;color:#33414a}
  #closing{position:absolute;left:60px;top:700px;width:420px;text-align:center;background:#ffcf3f;color:#122019;border:3px solid #1a1d20;border-radius:16px;padding:16px 10px;z-index:6}
  #closing b{font-size:20px;letter-spacing:.5px}
  #closing p{margin:6px 0 0;font-size:14px;font-weight:700}
  #sub{position:absolute;left:20px;right:20px;bottom:14px;min-height:58px;background:rgba(8,18,16,.88);border:1px solid rgba(255,255,255,.28);border-radius:12px;padding:10px 14px;z-index:11;font-size:16px;font-weight:700;line-height:1.35;text-align:center;color:#fff}
</style></head>
<body>
<div id="stage">
  <div id="camera">
    <svg id="sceneSvg" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse" patternTransform="rotate(-18)">
          <path d="M44 0H0V44" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="1.5"/>
        </pattern>
      </defs>
      <rect x="0" y="0" width="540" height="960" fill="#2e7d5b"/>
      <rect x="0" y="0" width="540" height="960" fill="url(#grid)"/>
      <!-- properti meja statis -->
      <g transform="translate(372,300) rotate(-18)">
        <rect x="0" y="0" width="172" height="30" rx="4" fill="#f2c94c" stroke="#1a1d20" stroke-width="2"/>
        <g stroke="#1a1d20" stroke-width="1.5"><line x1="16" y1="0" x2="16" y2="12"/><line x1="56" y1="0" x2="56" y2="12"/><line x1="96" y1="0" x2="96" y2="12"/><line x1="136" y1="0" x2="136" y2="12"/></g>
      </g>
      <g transform="translate(52,748) rotate(7)">
        <rect x="0" y="0" width="208" height="168" fill="#ffffff" opacity="0.92" stroke="#c5ced6" stroke-width="2"/>
        <g stroke="#d7dee4" stroke-width="2"><line x1="18" y1="34" x2="190" y2="34"/><line x1="18" y1="62" x2="190" y2="62"/><line x1="18" y1="90" x2="190" y2="90"/></g>
      </g>
      <g transform="translate(330,800) rotate(-14)">
        <rect x="0" y="0" width="150" height="12" rx="6" fill="#e8a33d" stroke="#1a1d20" stroke-width="2"/>
        <polygon points="150,0 168,6 150,12" fill="#f5d7a8" stroke="#1a1d20" stroke-width="2"/>
      </g>

      <!-- tali jam (belakang) -->
      <rect x="222" y="212" width="96" height="104" rx="12" fill="#5a3a22" stroke="#1a1d20" stroke-width="2.5"/>
      <rect x="222" y="668" width="96" height="104" rx="12" fill="#5a3a22" stroke="#1a1d20" stroke-width="2.5"/>
      <line x1="240" y1="212" x2="240" y2="316" stroke="#3a2415" stroke-width="2"/>
      <line x1="300" y1="212" x2="300" y2="316" stroke="#3a2415" stroke-width="2"/>

      <!-- bayangan lembut di bawah jam -->
      <ellipse cx="270" cy="700" rx="200" ry="16" fill="rgba(0,0,0,0.28)"/>

      <!-- casing jam -->
      <circle cx="270" cy="490" r="198" fill="#d8b25a" stroke="#1a1d20" stroke-width="3"/>
      <circle cx="270" cy="490" r="188" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2"/>
      <circle cx="270" cy="490" r="185" fill="#c9a227" stroke="#1a1d20" stroke-width="2.5"/>
      <!-- crown -->
      <rect x="462" y="478" width="22" height="24" rx="3" fill="#d8b25a" stroke="#1a1d20" stroke-width="2.5"/>
      <circle cx="488" cy="490" r="13" fill="#b8933f" stroke="#1a1d20" stroke-width="2.5"/>
      <!-- sekrup pelat -->
      <circle cx="270" cy="318" r="6" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2"/>
      <circle cx="270" cy="662" r="6" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2"/>
      <circle cx="98" cy="490" r="6" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2"/>
      <circle cx="442" cy="490" r="6" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2"/>

      <!-- SELURUH movement disembunyikan selama dial masih terpasang (adegan 0):
           dial menutupi movement; komponen yang menonjol keluar dial terlihat cacat.
           movementGroup opacity 0 -> 1 saat dial terangkat (2.2-3.5 dtk). -->
      <g id="movementGroup">
      <!-- BARREL / PEGAS UTAMA (185,400) r58: drum + lilitan pegas baja -->
      <g transform="translate(185,400)"><g id="barrelRot">
        <circle r="62" fill="#8a6d1f" stroke="#1a1d20" stroke-width="2.5"/>
        <circle r="58" fill="#d4af37" stroke="#1a1d20" stroke-width="2.5"/>
        <path d="__SPIRAL_BARREL__" fill="none" stroke="#5a4a12" stroke-width="4" stroke-linecap="round"/>
        <path d="__SPIRAL_BARREL__" fill="none" stroke="#f5d76e" stroke-width="1.5" stroke-linecap="round"/>
        <circle r="10" fill="#eef2f5" stroke="#1a1d20" stroke-width="2.5"/>
        <circle r="3" fill="#1a1d20"/>
      </g></g>

      <!-- RANTAI RODA GIGI -->
      __GEAR_CENTER__
      __GEAR_THIRD__
      __GEAR_FOURTH__
      <!-- ESCAPE WHEEL (195,570) gigi runcing 15 -->
      __GEAR_ESCAPE__

      <!-- jembatan pelat (di atas roda gigi, seperti movement asli) -->
      <g transform="translate(262,428) rotate(-8)">
        <rect x="-110" y="-13" width="220" height="26" rx="13" fill="#a8842a" stroke="#1a1d20" stroke-width="2.5"/>
        <circle cx="-88" cy="0" r="5" fill="#eef2f5" stroke="#1a1d20" stroke-width="2"/>
        <circle cx="88" cy="0" r="5" fill="#eef2f5" stroke="#1a1d20" stroke-width="2"/>
      </g>
      <g transform="translate(258,562) rotate(5)">
        <rect x="-95" y="-12" width="190" height="24" rx="12" fill="#a8842a" stroke="#1a1d20" stroke-width="2.5"/>
        <circle cx="-72" cy="0" r="5" fill="#eef2f5" stroke="#1a1d20" stroke-width="2"/>
        <circle cx="72" cy="0" r="5" fill="#eef2f5" stroke="#1a1d20" stroke-width="2"/>
      </g>

      <!-- PALLET FORK / JANGKAR (pivot 280,605) -->
      <g transform="translate(280,605)"><g id="palletRot">
        <path d="M-52,-38 L-8,-6 L-46,26 L-58,14 Z" fill="#d7dee4" stroke="#1a1d20" stroke-width="2.5"/>
        <path d="M-52,-38 L-8,-6 L-46,26 L-58,14 Z" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.6"/>
        <path d="M8,-6 L52,-14 L48,2 L8,6 Z" fill="#d7dee4" stroke="#1a1d20" stroke-width="2.5"/>
        <rect x="-56" y="-42" width="12" height="10" rx="2" fill="#c0392b" stroke="#1a1d20" stroke-width="2"/>
        <rect x="-50" y="18" width="12" height="10" rx="2" fill="#c0392b" stroke="#1a1d20" stroke-width="2"/>
        <circle r="9" fill="#eef2f5" stroke="#1a1d20" stroke-width="2.5"/>
        <circle r="3" fill="#1a1d20"/>
      </g></g>

      <!-- BALANCE WHEEL (360,595) r50 + pegas spiral — di dalam pelat -->
      <g transform="translate(360,595)">
        <g id="springGroup">
          <path d="__SPIRAL_HAIR__" fill="none" stroke="#3a6ea5" stroke-width="2.5" stroke-linecap="round"/>
        </g>
        <g id="balanceRot">
          <circle r="50" fill="none" stroke="#1a1d20" stroke-width="3"/>
          <circle r="47" fill="none" stroke="#d7dee4" stroke-width="9"/>
          <circle r="47" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.7"/>
          <line x1="-47" y1="0" x2="47" y2="0" stroke="#1a1d20" stroke-width="4"/>
          <line x1="0" y1="-47" x2="0" y2="47" stroke="#1a1d20" stroke-width="4"/>
          <circle cx="0" cy="-47" r="6" fill="#f2c94c" stroke="#1a1d20" stroke-width="2"/>
          <circle cx="0" cy="47" r="6" fill="#f2c94c" stroke="#1a1d20" stroke-width="2"/>
          <circle cx="-47" cy="0" r="6" fill="#f2c94c" stroke="#1a1d20" stroke-width="2"/>
          <circle cx="47" cy="0" r="6" fill="#f2c94c" stroke="#1a1d20" stroke-width="2"/>
          <circle r="9" fill="#eef2f5" stroke="#1a1d20" stroke-width="2.5"/>
          <circle r="3" fill="#1a1d20"/>
        </g>
      </g>

      <!-- JARUM DETIK (poros 270,490) -->
      <g transform="translate(270,490)"><g id="secRot">
        <polygon points="0,-152 -5,-20 -3,26 3,26 5,-20" fill="#c0392b" stroke="#1a1d20" stroke-width="2"/>
        <circle r="10" fill="#eef2f5" stroke="#1a1d20" stroke-width="2.5"/>
        <circle r="3" fill="#1a1d20"/>
      </g></g>

      <!-- lingkaran sorot per babak -->
      <circle id="hlBarrel" cx="185" cy="400" r="72" fill="none" stroke="#ffcf3f" stroke-width="3" stroke-dasharray="8 6"/>
      <circle id="hlGears" cx="300" cy="480" r="112" fill="none" stroke="#ffcf3f" stroke-width="3" stroke-dasharray="8 6"/>
      <circle id="hlEscape" cx="195" cy="570" r="50" fill="none" stroke="#ffcf3f" stroke-width="3" stroke-dasharray="8 6"/>
      <circle id="hlBalance" cx="360" cy="595" r="58" fill="none" stroke="#ffcf3f" stroke-width="3" stroke-dasharray="8 6"/>

      <!-- garis callout -->
      <line id="linePegas" x1="138" y1="372" x2="206" y2="322" stroke="#ffcf3f" stroke-width="3"/>
      <circle id="dotPegas" cx="138" cy="372" r="6" fill="#ffcf3f" stroke="#1a1d20" stroke-width="2"/>
      <line id="lineRantai" x1="322" y1="392" x2="318" y2="322" stroke="#ffcf3f" stroke-width="3"/>
      <circle id="dotRantai" cx="322" cy="392" r="6" fill="#ffcf3f" stroke="#1a1d20" stroke-width="2"/>
      <line id="lineEscape" x1="172" y1="586" x2="160" y2="324" stroke="#ffcf3f" stroke-width="3"/>
      <circle id="dotEscape" cx="172" cy="586" r="6" fill="#ffcf3f" stroke="#1a1d20" stroke-width="2"/>
      <line id="lineBalance" x1="388" y1="565" x2="328" y2="724" stroke="#ffcf3f" stroke-width="3"/>
      <circle id="dotBalance" cx="388" cy="565" r="6" fill="#ffcf3f" stroke="#1a1d20" stroke-width="2"/>
      </g><!-- /movementGroup -->

      <!-- DIAL jam utuh (terangkat saat dibongkar, adegan 0 saja) -->
      <g id="dialGroup">
        <circle cx="270" cy="490" r="165" fill="#f7f3e8" stroke="#1a1d20" stroke-width="3"/>
        <g stroke="#1a1d20" stroke-width="3">
          <line x1="270" y1="338" x2="270" y2="356"/><line x1="270" y1="624" x2="270" y2="642"/>
          <line x1="118" y1="490" x2="136" y2="490"/><line x1="404" y1="490" x2="422" y2="490"/>
        </g>
        <g stroke="#5a666e" stroke-width="2">
          <line x1="346" y1="358" x2="338" y2="372"/><line x1="422" y1="414" x2="408" y2="422"/>
          <line x1="194" y1="358" x2="202" y2="372"/><line x1="118" y1="414" x2="132" y2="422"/>
          <line x1="346" y1="622" x2="338" y2="608"/><line x1="422" y1="566" x2="408" y2="558"/>
          <line x1="194" y1="622" x2="202" y2="608"/><line x1="118" y1="566" x2="132" y2="558"/>
        </g>
        <text x="270" y="392" text-anchor="middle" font-size="26" font-weight="800" fill="#1a1d20">12</text>
        <text x="392" y="499" text-anchor="middle" font-size="26" font-weight="800" fill="#1a1d20">3</text>
        <text x="270" y="612" text-anchor="middle" font-size="26" font-weight="800" fill="#1a1d20">6</text>
        <text x="148" y="499" text-anchor="middle" font-size="26" font-weight="800" fill="#1a1d20">9</text>
        <text x="270" y="440" text-anchor="middle" font-size="13" font-weight="800" letter-spacing="2" fill="#5a666e">MEKANIK</text>
        <line x1="270" y1="490" x2="222" y2="442" stroke="#1a1d20" stroke-width="9" stroke-linecap="round"/>
        <line x1="270" y1="490" x2="336" y2="424" stroke="#1a1d20" stroke-width="7" stroke-linecap="round"/>
        <g id="dialSecRot"><line x1="270" y1="490" x2="270" y2="352" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/></g>
        <circle cx="270" cy="490" r="9" fill="#1a1d20"/>
      </g>
    </svg>

    <div class="badge" id="badgePegas" style="left:34px;top:296px">PEGAS UTAMA<small>ENERGI DISIMPAN DI SINI</small></div>
    <div class="badge" id="badgeRantai" style="right:60px;top:296px">RANTAI RODA GIGI<small>ENERGI MENGALIR PELAN</small></div>
    <div class="badge" id="badgeEscape" style="left:34px;top:296px">ESCAPEMENT<small>GERBANG MIKRO</small></div>
    <div class="badge" id="badgeBalance" style="right:60px;top:700px">BALANCE WHEEL<small>PENENTU SATU DETIK</small></div>

    <div id="titleBig">
      <h1>BONGKAR: JAM TANGAN</h1>
      <p>Tanpa baterai. Tanpa listrik. Tanpa chip.</p>
    </div>

    <div id="diagramCard">
      <h3>GERBANG MIKRO: GIGI LOLOS SATU PER SATU</h3>
      <svg width="392" height="64" viewBox="0 0 392 64">
        <g id="diagEsc">
          <polygon points="20,32 34,18 48,32 34,46" fill="#d7dee4" stroke="#1a1d20" stroke-width="2"/>
          <polygon points="60,32 74,18 88,32 74,46" fill="#d7dee4" stroke="#1a1d20" stroke-width="2"/>
          <polygon points="100,32 114,18 128,32 114,46" fill="#ffcf3f" stroke="#1a1d20" stroke-width="2"/>
          <polygon points="140,32 154,18 168,32 154,46" fill="#d7dee4" stroke="#1a1d20" stroke-width="2"/>
        </g>
        <path d="M250 14 L250 50 M250 14 L282 30 M250 50 L282 30" fill="none" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/>
        <text x="300" y="36" font-size="15" font-weight="800" fill="#122019">1 GIGI</text>
        <text x="300" y="54" font-size="12" font-weight="700" fill="#5a666e">LOLOS</text>
      </svg>
      <p id="diagText">Setiap kali gerbang terbuka, satu gigi lolos — lalu gerbang menutup lagi.</p>
    </div>

    <div id="closing">
      <b>PEGAS + GERBANG + AYUNAN = 1 DETIK</b>
      <p>Satu ayunan penuh, satu detik terjaga.</p>
    </div>
  </div>

  <div class="hud" id="hudLeft">
    <div class="brand">BONGKAR: JAM TANGAN</div>
    <div class="babak" id="babakLabel">INTRO · JAM UTUH</div>
  </div>
  <div class="hud" id="hudRight">
    <div class="val" id="teleVal">0</div>
    <div class="lab" id="teleLab">WAKTU</div>
  </div>
  <div id="sub"></div>
</div>
<script>
  var $ = function(id){ return document.getElementById(id); };
  function ss(a,b,t){ if(t<=a) return 0; if(t>=b) return 1; var x=(t-a)/(b-a); return x*x*(3-2*x); }
  function sceneOf(t){
    if(t<5) return 0; if(t<9) return 1; if(t<13.8) return 2; if(t<25.8) return 3; if(t<34) return 4; if(t<40) return 5; return 6;
  }
  window.BOUNDS = [0,5,9,13.8,25.8,34,40,46];
  var CUES = __CUES__;
  var LABELS = ['INTRO · JAM UTUH','BABAK 1 · PEGAS UTAMA','BABAK 2 · RANTAI RODA GIGI','BABAK 3 · ESCAPEMENT','BABAK 4 · BALANCE WHEEL','BABAK 5 · TANPA BALANCE','PENUTUP'];
  var CAM = [[1.02,0,0],[1.10,8,10],[1.12,-4,0],[1.14,8,-10],[1.14,-12,-12],[1.06,0,0],[1.00,0,0]];
  function render(t){
    var sc = sceneOf(t);
    // ===== SINGLE STATE CONTROLLER =====
    // Ayunan balance: 1 Hz -> 2 detak per detik. Tiap detak = 1 gigi escape lolos (24 deg).
    var ph = 2*Math.PI*t;
    var beat = Math.floor(2*t);                 // jumlah detak sejak 0
    var frac = 2*t - beat;                      // posisi dalam detak berjalan
    var step = frac < 0.18 ? ss(0, 0.18, frac) : 1;  // gigi melangkah cepat di awal detak
    var escBase = 24 * (beat + step);           // sudut kumulatif escape wheel (deg)
    var run = 720 * ss(34, 37.5, t);            // adegan 5: lari liar +720 deg lalu berhenti
    var esc, sec;
    if (t < 37.5) { esc = escBase + run; sec = 3 * (beat + step) + run / 8; }
    else if (t < 40) { esc = 2520; sec = 315; }
    else { esc = 2520 + 48 * (t - 40); sec = 315 + 6 * (t - 40); }
    var balanceOn = (t < 34 || t >= 40) ? 1 : 0;
    var balAng = balanceOn ? 28 * Math.sin(ph) : 0;
    var forkAng = balanceOn ? 8 * Math.tanh(3 * Math.sin(ph)) : 0;
    var spring = balanceOn ? 1 + 0.04 * Math.sin(ph) : 1;
    var centerAng = -esc / 4, thirdAng = esc / 3, fourthAng = -esc / 2, barrelAng = -esc / 12;

    $('barrelRot').setAttribute('transform', 'rotate(' + barrelAng + ')');
    $('centerRot').setAttribute('transform', 'rotate(' + centerAng + ')');
    $('thirdRot').setAttribute('transform', 'rotate(' + thirdAng + ')');
    $('fourthRot').setAttribute('transform', 'rotate(' + fourthAng + ')');
    $('escapeRot').setAttribute('transform', 'rotate(' + esc + ')');
    $('balanceRot').setAttribute('transform', 'rotate(' + balAng + ')');
    $('springGroup').setAttribute('transform', 'scale(' + spring + ')');
    $('palletRot').setAttribute('transform', 'rotate(' + forkAng + ')');
    $('secRot').setAttribute('transform', 'rotate(' + sec + ')');
    $('dialSecRot').setAttribute('transform', 'rotate(' + sec + ' 270 490)');
    // balance + pallet menghilang di adegan 5 (tanpa balance wheel)
    var balOp = 1 - ss(34, 34.8, t) * (1 - ss(39.6, 40, t));
    $('balanceRot').style.opacity = balOp;
    $('springGroup').style.opacity = balOp;
    $('palletRot').style.opacity = balOp;
    // diagram escapement: gigi kuning bergerak maju seiring lolosnya gigi
    $('diagEsc').setAttribute('transform', 'translate(' + ((esc % 40) - 20) + ' 0)');

    // dial terangkat saat dibongkar; movement muncul bersamaan (sembunyi saat dial terpasang)
    var lift = ss(2.2, 3.5, t);
    $('dialGroup').style.opacity = 1 - lift;
    $('dialGroup').setAttribute('transform', 'translate(0 ' + (-140 * lift) + ')');
    $('movementGroup').style.opacity = lift;

    // kamera: zoom/pan 2D saja, maks 1.14x, transisi halus 1 detik di awal babak
    var starts = [0, 5, 9, 13.8, 25.8, 34, 40];
    var prev = sc === 0 ? CAM[0] : CAM[sc - 1], cur = CAM[sc];
    var k = ss(starts[sc], starts[sc] + 1, t);
    var s = prev[0] + (cur[0] - prev[0]) * k;
    var tx = prev[1] + (cur[1] - prev[1]) * k;
    var ty = prev[2] + (cur[2] - prev[2]) * k;
    $('camera').style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + s + ')';

    // HUD + label babak
    $('babakLabel').textContent = LABELS[sc];
    var val, lab;
    if (sc === 0) { val = Math.round(t) + ' dtk'; lab = 'WAKTU'; }
    else if (sc === 1) { val = Math.round(100 - t * 0.5) + '%'; lab = 'ENERGI PEGAS'; }
    else if (sc === 2) { val = Math.round(((centerAng % 360) + 360) % 360) + '°'; lab = 'RODA GIGI'; }
    else if (sc === 3 || sc === 5) { val = Math.round(esc / 24); lab = 'GIGI LOLOS'; }
    else if (sc === 4) { val = Math.round(balAng) + '°'; lab = 'SUDUT AYUN'; }
    else { val = '2'; lab = 'DETAK / DETIK'; }
    $('teleVal').textContent = val; $('teleLab').textContent = lab;

    // sorot komponen + callout (muncul sekali per babak, lalu diam)
    function pair(badge, line, dot, v){ $(badge).style.opacity = v; $(line).style.opacity = v; $(dot).style.opacity = v; }
    var vPegas = Math.max(ss(5.2, 6, t) * (1 - ss(8.4, 9, t)), sc === 5 ? ss(34.2, 35, t) * (1 - ss(39.4, 40, t)) : 0);
    var vRantai = ss(9.2, 10, t) * (1 - ss(13.2, 13.8, t));
    var vEsc = ss(14, 14.8, t) * (1 - ss(25, 25.8, t));
    var vBal = ss(26, 26.8, t) * (1 - ss(33.4, 34, t));
    pair('badgePegas', 'linePegas', 'dotPegas', vPegas);
    pair('badgeRantai', 'lineRantai', 'dotRantai', vRantai);
    pair('badgeEscape', 'lineEscape', 'dotEscape', vEsc);
    pair('badgeBalance', 'lineBalance', 'dotBalance', vBal);
    $('hlBarrel').style.opacity = Math.max(ss(5.2, 6, t) * (1 - ss(8.4, 9, t)), sc === 5 ? 0.9 : 0);
    $('hlGears').style.opacity = ss(9.2, 10, t) * (1 - ss(13.2, 13.8, t));
    $('hlEscape').style.opacity = ss(14, 14.8, t) * (1 - ss(25, 25.8, t));
    $('hlBalance').style.opacity = ss(26, 26.8, t) * (1 - ss(33.4, 34, t));

    // judul, kartu diagram, penutup
    $('titleBig').style.opacity = ss(0.3, 1, t) * (1 - ss(4.2, 5, t));
    $('diagramCard').style.opacity = sc === 3 ? ss(15, 15.6, t) * (1 - ss(24.8, 25.8, t)) : 0;
    $('closing').style.opacity = sc === 6 ? ss(43.5, 44.5, t) : 0;

    // subtitle dari CUES (timing segmen transkripsi aktual)
    var txt = '';
    for (var i = 0; i < CUES.length; i++) {
      if (t >= CUES[i].start - 0.05 && t < CUES[i].end + 0.4) { txt = CUES[i].text; break; }
    }
    if ($('sub').textContent !== txt) $('sub').textContent = txt;
  }
  render(0);
</script>
</body></html>
"""

html = html.replace("__SPIRAL_BARREL__", spiral_path(8, 48, 3.2))
html = html.replace("__SPIRAL_HAIR__", spiral_path(6, 38, 4.5))
html = html.replace("__GEAR_CENTER__", gear_group("centerRot", 295, 410, 32, 38, 12, "#d4af37", spokes=4, hub=9))
html = html.replace("__GEAR_THIRD__", gear_group("thirdRot", 340, 480, 25, 30, 10, "#d7dee4", spokes=4, hub=8))
html = html.replace("__GEAR_FOURTH__", gear_group("fourthRot", 320, 540, 21, 26, 10, "#d4af37", spokes=4, hub=8))
html = html.replace("__GEAR_ESCAPE__", gear_group("escapeRot", 195, 570, 26, 38, 15, "#cfd8dc", spokes=0, hub=8, escape=True))
html = html.replace("__CUES__", CUES_JS)

open("animatic.html", "w").write(html)
print("animatic.html ditulis:", len(html), "byte")
