import os
import json
import base64
import re
import zipfile

ROOT_DIR = r'C:\Projects\prasannakaragar'
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
DOCS_DIR = os.path.join(ROOT_DIR, 'docs', 'font-licenses')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')

# 1. Load Base64 assets
with open(os.path.join(ASSETS_DIR, 'id.png'), 'rb') as f:
    id_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(os.path.join(ASSETS_DIR, 'right_pointing.png'), 'rb') as f:
    rp_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(os.path.join(DOCS_DIR, 'SpaceGrotesk-Bold.woff2'), 'rb') as f:
    sg_b64 = base64.b64encode(f.read()).decode('utf-8')

with open(os.path.join(DOCS_DIR, 'JetBrainsMono-SemiBold.woff2'), 'rb') as f:
    jbm_b64 = base64.b64encode(f.read()).decode('utf-8')

# Font Face CSS definition to include in SVGs
FONT_CSS = f"""
    @font-face {{
      font-family: 'Space Grotesk';
      font-style: normal;
      font-weight: 700;
      src: url('data:font/woff2;base64,{sg_b64}') format('woff2');
    }}
    @font-face {{
      font-family: 'JetBrains Mono';
      font-style: normal;
      font-weight: 600;
      src: url('data:font/woff2;base64,{jbm_b64}') format('woff2');
    }}
"""

# Extract SVG paths from Simple Icons cache
with open(os.path.join(SCRIPTS_DIR, 'simple_icons_cache.json'), 'r', encoding='utf-8') as f:
    icons_raw = json.load(f)

ICON_PATHS = {}
for k, v in icons_raw.items():
    m = re.search(r'd="([^"]+)"', v)
    if m:
        ICON_PATHS[k] = m.group(1)

# Ensure linkedin path is present
ICON_PATHS['linkedin'] = "M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.4 1.4 0 1 0 0-2.8 1.4 1.4 0 0 0 0 2.8m-1.4 9.74h2.8v-8.37H5.06v8.37Z"
ICON_PATHS['mail'] = "M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"

print(f"Loaded {len(ICON_PATHS)} icon paths.")

# ==========================================
# 1. BUILD HERO.SVG
# ==========================================
def build_hero():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 400" width="100%" height="100%">
  <defs>
    <style>
{FONT_CSS}
      .hero-font-display {{ font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      .hero-font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}

      /* Base keyframe animations */
      @keyframes heroFadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}

      @keyframes heroBlink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}

      @keyframes heroFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-7px); }}
      }}

      @keyframes heroPulseGlow {{
        0%, 100% {{ opacity: 0.35; transform: scale(1); }}
        50% {{ opacity: 0.6; transform: scale(1.05); }}
      }}

      /* 4 Cycling Roles (12s total: 3s each) */
      @keyframes heroRole1 {{
        0%, 22% {{ opacity: 1; transform: translateY(0); }}
        25%, 97% {{ opacity: 0; transform: translateY(-8px); }}
        98%, 100% {{ opacity: 0; transform: translateY(8px); }}
      }}
      @keyframes heroRole2 {{
        0%, 22% {{ opacity: 0; transform: translateY(8px); }}
        25%, 47% {{ opacity: 1; transform: translateY(0); }}
        50%, 100% {{ opacity: 0; transform: translateY(-8px); }}
      }}
      @keyframes heroRole3 {{
        0%, 47% {{ opacity: 0; transform: translateY(8px); }}
        50%, 72% {{ opacity: 1; transform: translateY(0); }}
        75%, 100% {{ opacity: 0; transform: translateY(-8px); }}
      }}
      @keyframes heroRole4 {{
        0%, 72% {{ opacity: 0; transform: translateY(8px); }}
        75%, 97% {{ opacity: 1; transform: translateY(0); }}
        98%, 100% {{ opacity: 0; transform: translateY(-8px); }}
      }}

      .hero-role-1 {{ animation: heroRole1 12s infinite; animation-fill-mode: both; }}
      .hero-role-2 {{ animation: heroRole2 12s infinite; animation-fill-mode: both; }}
      .hero-role-3 {{ animation: heroRole3 12s infinite; animation-fill-mode: both; }}
      .hero-role-4 {{ animation: heroRole4 12s infinite; animation-fill-mode: both; }}

      .hero-cursor {{ animation: heroBlink 1s infinite; }}
      .hero-char-wrap {{ animation: heroFloat 5s ease-in-out infinite; transform-origin: center center; }}
      .hero-glow-anim {{ animation: heroPulseGlow 4s ease-in-out infinite; transform-origin: 670px 200px; }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
        .hero-role-1 {{ opacity: 1 !important; transform: none !important; }}
        .hero-role-2, .hero-role-3, .hero-role-4 {{ display: none !important; }}
      }}
    </style>

    <!-- Dot Grid Pattern -->
    <pattern id="hero-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#1b2942" opacity="0.6"/>
    </pattern>

    <!-- Linear Gradients -->
    <linearGradient id="hero-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a101f"/>
      <stop offset="100%" stop-color="#050811"/>
    </linearGradient>

    <linearGradient id="hero-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.6"/>
      <stop offset="50%" stop-color="#23334d" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.5"/>
    </linearGradient>

    <linearGradient id="hero-name-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#f5f7ff"/>
      <stop offset="100%" stop-color="#9dc1ff"/>
    </linearGradient>

    <linearGradient id="hero-badge-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.15"/>
    </linearGradient>

    <!-- Ambient Glow Radials -->
    <radialGradient id="hero-blue-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.45"/>
      <stop offset="70%" stop-color="#247bff" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="hero-crimson-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ff354f" stop-opacity="0.4"/>
      <stop offset="70%" stop-color="#ff354f" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0"/>
    </radialGradient>

    <!-- Rising Mask for Name Reveal -->
    <clipPath id="hero-name-clip">
      <rect x="40" y="88" width="520" height="66">
        <animate attributeName="y" values="160; 88" dur="1.2s" fill="freeze" calcMode="spline" keyTimes="0; 1" keySplines="0.16 1 0.3 1"/>
      </rect>
    </clipPath>

    <!-- Portrait Arch Clip -->
    <clipPath id="hero-portrait-clip">
      <rect x="530" y="30" width="290" height="340" rx="20"/>
    </clipPath>
  </defs>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="400" rx="16" fill="url(#hero-bg-grad)"/>
  <rect x="0" y="0" width="850" height="400" rx="16" fill="url(#hero-dots)"/>
  <rect x="0.5" y="0.5" width="849" height="399" rx="15.5" fill="none" stroke="url(#hero-border-grad)" stroke-width="1.2"/>

  <!-- Left Glowing Aura -->
  <circle cx="120" cy="80" r="180" fill="url(#hero-blue-glow)"/>

  <!-- Right Character Glowing Aura -->
  <g class="hero-glow-anim">
    <circle cx="670" cy="210" r="160" fill="url(#hero-blue-glow)"/>
    <circle cx="710" cy="230" r="140" fill="url(#hero-crimson-glow)"/>
  </g>

  <!-- ================= LEFT CONTENT ================= -->

  <!-- Terminal Header / Status Pill -->
  <g transform="translate(42, 38)">
    <rect x="0" y="0" width="210" height="26" rx="13" fill="#101c30" stroke="#23334d" stroke-width="1"/>
    <circle cx="14" cy="13" r="4" fill="#ff354f"/>
    <circle cx="26" cy="13" r="4" fill="#ffb835"/>
    <circle cx="38" cy="13" r="4" fill="#00e599"/>
    <text x="52" y="17" fill="#8995ad" class="hero-font-mono" font-size="11" font-weight="600" letter-spacing="0.5">prasanna.dev / live</text>
  </g>

  <g transform="translate(262, 38)">
    <rect x="0" y="0" width="170" height="26" rx="13" fill="#101c30" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
    <circle cx="14" cy="13" r="3.5" fill="#247bff">
      <animate attributeName="opacity" values="1; 0.4; 1" dur="2s" repeatCount="indefinite"/>
    </circle>
    <text x="26" y="17" fill="#247bff" class="hero-font-mono" font-size="10.5" font-weight="600" letter-spacing="0.8">BANGALORE, IN</text>
  </g>

  <!-- Typed Greeting -->
  <g transform="translate(42, 86)">
    <text x="0" y="0" fill="#247bff" class="hero-font-mono" font-size="14" font-weight="600" letter-spacing="1">
      &gt; HELLO WORLD, I'M<tspan class="hero-cursor" fill="#ff354f">_</tspan>
    </text>
  </g>

  <!-- Large Animated Name Reveal with Rising Mask -->
  <g clip-path="url(#hero-name-clip)">
    <text x="42" y="142" fill="url(#hero-name-grad)" class="hero-font-display" font-size="46" font-weight="700" letter-spacing="-0.5">
      PRASANNA KARAGAR
    </text>
  </g>

  <!-- 4 Rotating Developer Roles Badge (Y=168) -->
  <g transform="translate(42, 168)">
    <rect x="0" y="0" width="340" height="32" rx="8" fill="url(#hero-badge-grad)" stroke="#247bff" stroke-width="1" stroke-opacity="0.4"/>
    <path d="M14 10 L22 10 L16 16 L22 16 L12 24 L14 17 L10 17 Z" fill="#ff354f"/>
    
    <g class="hero-role-1">
      <text x="32" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="13" font-weight="600" letter-spacing="1.2">BACKEND ENGINEER</text>
    </g>
    <g class="hero-role-2">
      <text x="32" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="13" font-weight="600" letter-spacing="1.2">DSA &amp; CP SPECIALIST</text>
    </g>
    <g class="hero-role-3">
      <text x="32" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="13" font-weight="600" letter-spacing="1.2">SYSTEM DESIGN ENTHUSIAST</text>
    </g>
    <g class="hero-role-4">
      <text x="32" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="13" font-weight="600" letter-spacing="1.2">FULL-STACK DEVELOPER</text>
    </g>
  </g>

  <!-- One-Line Professional Pitch (Y=226) -->
  <g transform="translate(42, 230)">
    <text x="0" y="0" fill="#8995ad" class="hero-font-display" font-size="14.5" font-weight="400">
      <tspan x="0" dy="0">Information Science undergraduate at REVA University building scalable</tspan>
      <tspan x="0" dy="22">backend systems, competitive programming engines, and secure platforms.</tspan>
    </text>
  </g>

  <!-- Location & Verification Pills Row (Y=288) -->
  <g transform="translate(42, 288)">
    <!-- Pill 1: Education -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="220" height="34" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <text x="14" y="21" fill="#247bff" font-size="14">🎓</text>
      <text x="36" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="11.5" font-weight="600">REVA UNIVERSITY</text>
      <text x="160" y="21" fill="#8995ad" class="hero-font-mono" font-size="11">'27</text>
    </g>

    <!-- Pill 2: Program -->
    <g transform="translate(230, 0)">
      <rect x="0" y="0" width="160" height="34" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <text x="14" y="21" fill="#ff354f" font-size="14">⚡</text>
      <text x="36" y="21" fill="#f5f7ff" class="hero-font-mono" font-size="11.5" font-weight="600">B.TECH ISE (2ND YR)</text>
    </g>

    <!-- Pill 3: Focus -->
    <g transform="translate(0, 44)">
      <rect x="0" y="0" width="390" height="32" rx="8" fill="#0c1626" stroke="#23334d" stroke-width="1"/>
      <text x="14" y="20" fill="#00e599" font-size="13">❖</text>
      <text x="34" y="20" fill="#8995ad" class="hero-font-mono" font-size="11">CORE: </text>
      <text x="82" y="20" fill="#f5f7ff" class="hero-font-mono" font-size="11" font-weight="600">C++ • NODE.JS • DOCKER • MYSQL • SYSTEM DESIGN</text>
    </g>
  </g>

  <!-- ================= RIGHT PORTRAIT ================= -->
  <g class="hero-char-wrap" transform="translate(520, 20)">
    <!-- Decorative Frame / Backdrop Card -->
    <rect x="15" y="15" width="280" height="340" rx="20" fill="#0e172a" stroke="#247bff" stroke-width="1.5" stroke-opacity="0.3"/>
    
    <!-- Accent Corner Marks -->
    <path d="M15 45 L15 25 Q15 15 25 15 L45 15" fill="none" stroke="#247bff" stroke-width="2.5"/>
    <path d="M265 15 L285 15 Q295 15 295 25 L295 45" fill="none" stroke="#ff354f" stroke-width="2.5"/>
    <path d="M295 325 L295 345 Q295 355 285 355 L265 355" fill="none" stroke="#247bff" stroke-width="2.5"/>
    <path d="M45 355 L25 355 Q15 355 15 345 L15 325" fill="none" stroke="#ff354f" stroke-width="2.5"/>

    <!-- Clipped Character Image -->
    <g clip-path="url(#hero-portrait-clip)">
      <image href="data:image/png;base64,{id_b64}" x="25" y="15" width="265" height="350" preserveAspectRatio="xMidYMid slice"/>
    </g>

    <!-- Floating ID Pill at bottom of portrait -->
    <g transform="translate(45, 324)">
      <rect x="0" y="0" width="220" height="26" rx="13" fill="#070b16" stroke="#247bff" stroke-width="1.2" opacity="0.95"/>
      <circle cx="14" cy="13" r="3.5" fill="#00e599"/>
      <text x="26" y="17" fill="#f5f7ff" class="hero-font-mono" font-size="10.5" font-weight="600" letter-spacing="1">ID: PRASANNA // VERIFIED</text>
    </g>
  </g>
</svg>"""
    return svg


# ==========================================
# 2. BUILD ABOUT-LIFE.SVG
# ==========================================
def build_about():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" height="100%">
  <defs>
    <style>
{FONT_CSS}
      .abt-font-display {{ font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      .abt-font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}

      /* 3-Slide Carousel Animation (12s cycle: 4s per slide) */
      @keyframes abtSlide1 {{
        0%, 30% {{ opacity: 1; transform: translateY(0); }}
        33.3%, 96.7% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
      }}
      @keyframes abtSlide2 {{
        0%, 30% {{ opacity: 0; transform: translateY(-10px); }}
        33.3%, 63.3% {{ opacity: 1; transform: translateY(0); }}
        66.6%, 100% {{ opacity: 0; transform: translateY(10px); }}
      }}
      @keyframes abtSlide3 {{
        0%, 63.3% {{ opacity: 0; transform: translateY(-10px); }}
        66.6%, 96.7% {{ opacity: 1; transform: translateY(0); }}
        100% {{ opacity: 0; transform: translateY(10px); }}
      }}

      /* Progress Bar Animations */
      @keyframes abtProgress1 {{
        0% {{ width: 0px; }}
        33.3% {{ width: 115px; }}
        33.4%, 100% {{ width: 0px; }}
      }}
      @keyframes abtProgress2 {{
        0%, 33.3% {{ width: 0px; }}
        66.6% {{ width: 115px; }}
        66.7%, 100% {{ width: 0px; }}
      }}
      @keyframes abtProgress3 {{
        0%, 66.6% {{ width: 0px; }}
        99.9% {{ width: 115px; }}
        100% {{ width: 0px; }}
      }}

      .abt-s1 {{ animation: abtSlide1 12s infinite; animation-fill-mode: both; }}
      .abt-s2 {{ animation: abtSlide2 12s infinite; animation-fill-mode: both; }}
      .abt-s3 {{ animation: abtSlide3 12s infinite; animation-fill-mode: both; }}

      .abt-bar-1 {{ animation: abtProgress1 12s infinite linear; }}
      .abt-bar-2 {{ animation: abtProgress2 12s infinite linear; }}
      .abt-bar-3 {{ animation: abtProgress3 12s infinite linear; }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
        .abt-s1 {{ opacity: 1 !important; transform: none !important; }}
        .abt-s2, .abt-s3 {{ display: none !important; }}
        .abt-bar-1 {{ width: 115px !important; }}
      }}
    </style>

    <pattern id="abt-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#1b2942" opacity="0.6"/>
    </pattern>

    <linearGradient id="abt-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a101f"/>
      <stop offset="100%" stop-color="#050811"/>
    </linearGradient>

    <linearGradient id="abt-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#23334d" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.4"/>
    </linearGradient>

    <radialGradient id="abt-blue-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Card Background -->
  <rect x="0" y="0" width="850" height="360" rx="16" fill="url(#abt-bg-grad)"/>
  <rect x="0" y="0" width="850" height="360" rx="16" fill="url(#abt-dots)"/>
  <rect x="0.5" y="0.5" width="849" height="359" rx="15.5" fill="none" stroke="url(#abt-border-grad)" stroke-width="1.2"/>

  <!-- Ambient Glow in Center -->
  <circle cx="425" cy="180" r="240" fill="url(#abt-blue-glow)"/>

  <!-- Section Header -->
  <g transform="translate(40, 36)">
    <rect x="0" y="0" width="8" height="8" rx="2" fill="#247bff"/>
    <text x="18" y="8" fill="#247bff" class="abt-font-mono" font-size="11" font-weight="600" letter-spacing="1.5">SECTION 02 // ABOUT &amp; FOCUS</text>
  </g>

  <!-- ================= LEFT COLUMN: CAPABILITIES & ARCHITECTURE ================= -->
  <g transform="translate(40, 70)">
    <text x="0" y="24" fill="#f5f7ff" class="abt-font-display" font-size="22" font-weight="700" letter-spacing="-0.3">
      ENGINEERING PHILOSOPHY
    </text>

    <text x="0" y="52" fill="#8995ad" class="abt-font-display" font-size="13.5" font-weight="400">
      <tspan x="0" dy="0">Second-year Information Science student deeply invested in</tspan>
      <tspan x="0" dy="20">algorithmic rigor and scalable backend engineering. Passionate</tspan>
      <tspan x="0" dy="20">about writing efficient code, distributed systems, and real-time</tspan>
      <tspan x="0" dy="20">examination telemetry platforms.</tspan>
    </text>

    <!-- Key Capability Cards -->
    <g transform="translate(0, 134)">
      <!-- Item 1 -->
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="370" height="42" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <circle cx="20" cy="21" r="10" fill="#247bff" fill-opacity="0.2"/>
        <text x="16" y="25" fill="#247bff" font-size="11">⚡</text>
        <text x="38" y="25" fill="#f5f7ff" class="abt-font-mono" font-size="11.5" font-weight="600">HIGH-PERFORMANCE BACKEND</text>
        <text x="245" y="25" fill="#8995ad" class="abt-font-mono" font-size="10.5">Node • Express • APIs</text>
      </g>

      <!-- Item 2 -->
      <g transform="translate(0, 50)">
        <rect x="0" y="0" width="370" height="42" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <circle cx="20" cy="21" r="10" fill="#ff354f" fill-opacity="0.2"/>
        <text x="15" y="25" fill="#ff354f" font-size="11">🧠</text>
        <text x="38" y="25" fill="#f5f7ff" class="abt-font-mono" font-size="11.5" font-weight="600">DSA &amp; PROBLEM SOLVING</text>
        <text x="245" y="25" fill="#8995ad" class="abt-font-mono" font-size="10.5">C++ • DP • Graphs</text>
      </g>

      <!-- Item 3 -->
      <g transform="translate(0, 100)">
        <rect x="0" y="0" width="370" height="42" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <circle cx="20" cy="21" r="10" fill="#00e599" fill-opacity="0.2"/>
        <text x="15" y="25" fill="#00e599" font-size="11">🛡️</text>
        <text x="38" y="25" fill="#f5f7ff" class="abt-font-mono" font-size="11.5" font-weight="600">INTEGRITY &amp; SANDBOXES</text>
        <text x="245" y="25" fill="#8995ad" class="abt-font-mono" font-size="10.5">Judge0 • Docker • RBAC</text>
      </g>
    </g>
  </g>

  <!-- Vertical Divider -->
  <line x1="435" y1="65" x2="435" y2="330" stroke="#23334d" stroke-width="1" stroke-dasharray="3,3"/>

  <!-- ================= RIGHT COLUMN: 3-SLIDE CAROUSEL ================= -->
  <g transform="translate(460, 55)">
    <!-- Carousel Segment Progress Bars (3 segments) -->
    <g transform="translate(0, 0)">
      <!-- Segment 1 -->
      <g transform="translate(0, 0)">
        <rect x="0" y="0" width="115" height="4" rx="2" fill="#1b2942"/>
        <rect x="0" y="0" width="0" height="4" rx="2" fill="#247bff" class="abt-bar-1"/>
      </g>
      <!-- Segment 2 -->
      <g transform="translate(122, 0)">
        <rect x="0" y="0" width="115" height="4" rx="2" fill="#1b2942"/>
        <rect x="0" y="0" width="0" height="4" rx="2" fill="#247bff" class="abt-bar-2"/>
      </g>
      <!-- Segment 3 -->
      <g transform="translate(244, 0)">
        <rect x="0" y="0" width="115" height="4" rx="2" fill="#1b2942"/>
        <rect x="0" y="0" width="0" height="4" rx="2" fill="#ff354f" class="abt-bar-3"/>
      </g>
    </g>

    <!-- Slide Container (Card) -->
    <rect x="0" y="16" width="355" height="260" rx="12" fill="#0d1726" stroke="#23334d" stroke-width="1"/>

    <!-- ================= SLIDE 1 ================= -->
    <g class="abt-s1" transform="translate(24, 40)">
      <rect x="0" y="0" width="180" height="22" rx="4" fill="#247bff" fill-opacity="0.15"/>
      <text x="8" y="15" fill="#247bff" class="abt-font-mono" font-size="10.5" font-weight="600" letter-spacing="1">01 // CORE PASSION</text>
      
      <text x="0" y="48" fill="#f5f7ff" class="abt-font-display" font-size="19" font-weight="700">Competitive Programming</text>
      
      <text x="0" y="76" fill="#8995ad" class="abt-font-display" font-size="13">
        <tspan x="0" dy="0">Daily commitment to breaking down complex</tspan>
        <tspan x="0" dy="19">algorithmic challenges into optimal graph, tree,</tspan>
        <tspan x="0" dy="19">and dynamic programming solutions.</tspan>
      </text>

      <!-- Highlights Box -->
      <g transform="translate(0, 142)">
        <rect x="0" y="0" width="308" height="64" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <text x="14" y="24" fill="#247bff" class="abt-font-mono" font-size="11">✓ Active on LeetCode &amp; Codeforces</text>
        <text x="14" y="46" fill="#8995ad" class="abt-font-mono" font-size="11">✓ Focus: C++ STL &amp; Optimal Time Complexity</text>
      </g>
    </g>

    <!-- ================= SLIDE 2 ================= -->
    <g class="abt-s2" transform="translate(24, 40)">
      <rect x="0" y="0" width="200" height="22" rx="4" fill="#247bff" fill-opacity="0.15"/>
      <text x="8" y="15" fill="#247bff" class="abt-font-mono" font-size="10.5" font-weight="600" letter-spacing="1">02 // ARCHITECTURE &amp; BUILD</text>
      
      <text x="0" y="48" fill="#f5f7ff" class="abt-font-display" font-size="19" font-weight="700">Backend &amp; Code Engines</text>
      
      <text x="0" y="76" fill="#8995ad" class="abt-font-display" font-size="13">
        <tspan x="0" dy="0">Architecting automated code evaluation and</tspan>
        <tspan x="0" dy="19">proctoring pipelines like UniRank. Handling</tspan>
        <tspan x="0" dy="19">sandboxed execution with Docker &amp; Judge0.</tspan>
      </text>

      <!-- Highlights Box -->
      <g transform="translate(0, 142)">
        <rect x="0" y="0" width="308" height="64" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <text x="14" y="24" fill="#00e599" class="abt-font-mono" font-size="11">✓ Sandboxed Execution (Docker / Judge0)</text>
        <text x="14" y="46" fill="#8995ad" class="abt-font-mono" font-size="11">✓ Node.js • Express • MySQL Schemas</text>
      </g>
    </g>

    <!-- ================= SLIDE 3 ================= -->
    <g class="abt-s3" transform="translate(24, 40)">
      <rect x="0" y="0" width="205" height="22" rx="4" fill="#ff354f" fill-opacity="0.15"/>
      <text x="8" y="15" fill="#ff354f" class="abt-font-mono" font-size="10.5" font-weight="600" letter-spacing="1">03 // SYSTEMS &amp; INTEGRITY</text>
      
      <text x="0" y="48" fill="#f5f7ff" class="abt-font-display" font-size="19" font-weight="700">Secure Platform Telemetry</text>
      
      <text x="0" y="76" fill="#8995ad" class="abt-font-display" font-size="13">
        <tspan x="0" dy="0">Developing the Exam Portal platform with</tspan>
        <tspan x="0" dy="19">real-time anti-cheat event auditing, role-based</tspan>
        <tspan x="0" dy="19">access controls, and robust session security.</tspan>
      </text>

      <!-- Highlights Box -->
      <g transform="translate(0, 142)">
        <rect x="0" y="0" width="308" height="64" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <text x="14" y="24" fill="#ff354f" class="abt-font-mono" font-size="11">✓ Anti-Cheat &amp; Telemetry Audits</text>
        <text x="14" y="46" fill="#8995ad" class="abt-font-mono" font-size="11">✓ Role-Based Access Control (RBAC)</text>
      </g>
    </g>
  </g>
</svg>"""
    return svg


# ==========================================
# 3. BUILD STACK.SVG
# ==========================================
def build_stack():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 450" width="100%" height="100%">
  <defs>
    <style>
{FONT_CSS}
      .stk-font-display {{ font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      .stk-font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}

      /* Orbit Revolutions */
      @keyframes stkOrbitInner {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}
      @keyframes stkOrbitMid {{
        from {{ transform: rotate(360deg); }}
        to {{ transform: rotate(0deg); }}
      }}
      @keyframes stkOrbitOuter {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
      }}

      /* Counter-rotate to keep icons upright */
      @keyframes stkCounterInner {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(-360deg); }}
      }}
      @keyframes stkCounterMid {{
        from {{ transform: rotate(-360deg); }}
        to {{ transform: rotate(0deg); }}
      }}
      @keyframes stkCounterOuter {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(-360deg); }}
      }}

      @keyframes stkCorePulse {{
        0%, 100% {{ transform: scale(1); opacity: 0.9; }}
        50% {{ transform: scale(1.08); opacity: 1; }}
      }}

      .stk-rot-inner {{ animation: stkOrbitInner 20s linear infinite; transform-origin: 210px 230px; }}
      .stk-rot-mid {{ animation: stkOrbitMid 28s linear infinite; transform-origin: 210px 230px; }}
      .stk-rot-outer {{ animation: stkOrbitOuter 38s linear infinite; transform-origin: 210px 230px; }}

      .stk-cnt-inner {{ animation: stkCounterInner 20s linear infinite; }}
      .stk-cnt-mid {{ animation: stkCounterMid 28s linear infinite; }}
      .stk-cnt-outer {{ animation: stkCounterOuter 38s linear infinite; }}

      .stk-pulse {{ animation: stkCorePulse 4s ease-in-out infinite; transform-origin: 210px 230px; }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <pattern id="stk-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#1b2942" opacity="0.6"/>
    </pattern>

    <linearGradient id="stk-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a101f"/>
      <stop offset="100%" stop-color="#050811"/>
    </linearGradient>

    <linearGradient id="stk-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#23334d" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.4"/>
    </linearGradient>

    <radialGradient id="stk-center-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.4"/>
      <stop offset="60%" stop-color="#ff354f" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="850" height="450" rx="16" fill="url(#stk-bg-grad)"/>
  <rect x="0" y="0" width="850" height="450" rx="16" fill="url(#stk-dots)"/>
  <rect x="0.5" y="0.5" width="849" height="449" rx="15.5" fill="none" stroke="url(#stk-border-grad)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(40, 36)">
    <rect x="0" y="0" width="8" height="8" rx="2" fill="#247bff"/>
    <text x="18" y="8" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="600" letter-spacing="1.5">SECTION 03 // TECH STACK &amp; ORBITAL ARCHITECTURE</text>
  </g>

  <!-- ================= LEFT AREA: 3 TILTED ORBITAL SYSTEMS ================= -->
  <!-- Ambient Center Glow -->
  <circle cx="210" cy="235" r="160" fill="url(#stk-center-glow)"/>

  <!-- Static Orbit Ellipse Tracks -->
  <g stroke="#23334d" stroke-width="1.2" stroke-dasharray="4,4" fill="none" opacity="0.85">
    <!-- Inner Track (r=80) -->
    <ellipse cx="210" cy="235" rx="80" ry="75"/>
    <!-- Middle Track (r=130) -->
    <ellipse cx="210" cy="235" rx="130" ry="120" stroke="#2b3d5c"/>
    <!-- Outer Track (r=180) -->
    <ellipse cx="210" cy="235" rx="180" ry="165"/>
  </g>

  <!-- Central Glowing Core -->
  <g class="stk-pulse">
    <circle cx="210" cy="235" r="32" fill="#101c30" stroke="#247bff" stroke-width="2"/>
    <circle cx="210" cy="235" r="26" fill="#070b16"/>
    <text x="210" y="231" text-anchor="middle" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="700">CORE</text>
    <text x="210" y="244" text-anchor="middle" fill="#ff354f" class="stk-font-mono" font-size="9" font-weight="600">DSA/SYS</text>
  </g>

  <!-- ORBIT 1: INNER (Languages: C++, Python, JS, C) - r=80 -->
  <g class="stk-rot-inner">
    <!-- Node 1: C++ (0 deg: 210+80=290, 235) -->
    <g transform="translate(290, 235)">
      <g class="stk-cnt-inner" transform-origin="0 0">
        <circle cx="0" cy="0" r="17" fill="#101c30" stroke="#247bff" stroke-width="1.2"/>
        <path d="{ICON_PATHS['cplusplus']}" fill="#00599C" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 2: Python (90 deg: 210, 235+75=310) -->
    <g transform="translate(210, 310)">
      <g class="stk-cnt-inner" transform-origin="0 0">
        <circle cx="0" cy="0" r="17" fill="#101c30" stroke="#3776AB" stroke-width="1.2"/>
        <path d="{ICON_PATHS['python']}" fill="#3776AB" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 3: JavaScript (180 deg: 210-80=130, 235) -->
    <g transform="translate(130, 235)">
      <g class="stk-cnt-inner" transform-origin="0 0">
        <circle cx="0" cy="0" r="17" fill="#101c30" stroke="#F7DF1E" stroke-width="1.2"/>
        <path d="{ICON_PATHS['javascript']}" fill="#F7DF1E" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 4: C (270 deg: 210, 235-75=160) -->
    <g transform="translate(210, 160)">
      <g class="stk-cnt-inner" transform-origin="0 0">
        <circle cx="0" cy="0" r="17" fill="#101c30" stroke="#A8B9CC" stroke-width="1.2"/>
        <text x="0" y="4" text-anchor="middle" fill="#A8B9CC" class="stk-font-mono" font-size="11" font-weight="700">C</text>
      </g>
    </g>
  </g>

  <!-- ORBIT 2: MIDDLE (Backend & Data: Node, Express, MySQL, Docker) - rx=130, ry=120 -->
  <g class="stk-rot-mid">
    <!-- Node 1: Node.js (45 deg: ~210+92=302, 235+85=320) -->
    <g transform="translate(302, 320)">
      <g class="stk-cnt-mid" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#5FA04E" stroke-width="1.2"/>
        <path d="{ICON_PATHS['nodedotjs']}" fill="#5FA04E" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 2: Docker (135 deg: ~210-92=118, 235+85=320) -->
    <g transform="translate(118, 320)">
      <g class="stk-cnt-mid" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#2496ED" stroke-width="1.2"/>
        <path d="{ICON_PATHS['docker']}" fill="#2496ED" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 3: MySQL (225 deg: ~210-92=118, 235-85=150) -->
    <g transform="translate(118, 150)">
      <g class="stk-cnt-mid" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#4479A1" stroke-width="1.2"/>
        <path d="{ICON_PATHS['mysql']}" fill="#4479A1" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 4: Express (315 deg: ~210+92=302, 235-85=150) -->
    <g transform="translate(302, 150)">
      <g class="stk-cnt-mid" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#f5f7ff" stroke-width="1.2"/>
        <text x="0" y="4" text-anchor="middle" fill="#f5f7ff" class="stk-font-mono" font-size="9" font-weight="700">ex</text>
      </g>
    </g>
  </g>

  <!-- ORBIT 3: OUTER (Tools & Frontend: React, Git, GitHub, Postman) - rx=180, ry=165 -->
  <g class="stk-rot-outer">
    <!-- Node 1: React (0 deg: 210+180=390, 235) -->
    <g transform="translate(390, 235)">
      <g class="stk-cnt-outer" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#61DAFB" stroke-width="1.2"/>
        <path d="{ICON_PATHS['react']}" fill="#61DAFB" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 2: Postman (90 deg: 210, 235+165=400) -->
    <g transform="translate(210, 400)">
      <g class="stk-cnt-outer" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#FF6C37" stroke-width="1.2"/>
        <path d="{ICON_PATHS['postman']}" fill="#FF6C37" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 3: Git (180 deg: 210-180=30, 235) -->
    <g transform="translate(30, 235)">
      <g class="stk-cnt-outer" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#F05032" stroke-width="1.2"/>
        <path d="{ICON_PATHS['git']}" fill="#F05032" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>

    <!-- Node 4: GitHub (270 deg: 210, 235-165=70) -->
    <g transform="translate(210, 70)">
      <g class="stk-cnt-outer" transform-origin="0 0">
        <circle cx="0" cy="0" r="18" fill="#101c30" stroke="#f5f7ff" stroke-width="1.2"/>
        <path d="{ICON_PATHS['github']}" fill="#f5f7ff" transform="translate(-9, -9) scale(0.75)"/>
      </g>
    </g>
  </g>

  <!-- ================= RIGHT AREA: GROUPED STACK CHIPS ================= -->
  <g transform="translate(440, 65)">
    <!-- Category 1: Languages -->
    <g transform="translate(0, 0)">
      <text x="0" y="12" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="600" letter-spacing="1">PROGRAMMING LANGUAGES</text>
      <g transform="translate(0, 20)">
        <!-- C++ -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="85" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['cplusplus']}" fill="#00599C" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">C++</text>
        </g>
        <!-- C -->
        <g transform="translate(93, 0)">
          <rect x="0" y="0" width="65" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <text x="12" y="19" fill="#A8B9CC" class="stk-font-mono" font-size="12" font-weight="700">C</text>
          <text x="28" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Lang</text>
        </g>
        <!-- Python -->
        <g transform="translate(166, 0)">
          <rect x="0" y="0" width="100" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['python']}" fill="#3776AB" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Python</text>
        </g>
        <!-- JavaScript -->
        <g transform="translate(274, 0)">
          <rect x="0" y="0" width="105" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['javascript']}" fill="#F7DF1E" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">JavaScript</text>
        </g>
      </g>
    </g>

    <!-- Category 2: Backend & Systems -->
    <g transform="translate(0, 82)">
      <text x="0" y="12" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="600" letter-spacing="1">BACKEND &amp; SYSTEM DESIGN</text>
      <g transform="translate(0, 20)">
        <!-- Node.js -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="98" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['nodedotjs']}" fill="#5FA04E" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Node.js</text>
        </g>
        <!-- Express -->
        <g transform="translate(106, 0)">
          <rect x="0" y="0" width="95" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <text x="10" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Express.js</text>
        </g>
        <!-- Judge0 / Sandboxing -->
        <g transform="translate(209, 0)">
          <rect x="0" y="0" width="85" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <text x="10" y="19" fill="#00e599" font-size="11">⚡</text>
          <text x="26" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Judge0</text>
        </g>
        <!-- Docker -->
        <g transform="translate(302, 0)">
          <rect x="0" y="0" width="85" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['docker']}" fill="#2496ED" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Docker</text>
        </g>
      </g>
    </g>

    <!-- Category 3: Databases & Storage -->
    <g transform="translate(0, 164)">
      <text x="0" y="12" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="600" letter-spacing="1">DATABASES &amp; STORAGE</text>
      <g transform="translate(0, 20)">
        <!-- MySQL -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="95" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['mysql']}" fill="#4479A1" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">MySQL</text>
        </g>
        <!-- MongoDB -->
        <g transform="translate(103, 0)">
          <rect x="0" y="0" width="105" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['mongodb']}" fill="#47A248" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">MongoDB</text>
        </g>
        <!-- Supabase -->
        <g transform="translate(216, 0)">
          <rect x="0" y="0" width="105" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <text x="10" y="19" fill="#3ECF8E" font-size="11">❖</text>
          <text x="26" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Supabase</text>
        </g>
      </g>
    </g>

    <!-- Category 4: Frontend & Development Tools -->
    <g transform="translate(0, 246)">
      <text x="0" y="12" fill="#247bff" class="stk-font-mono" font-size="11" font-weight="600" letter-spacing="1">FRONTEND &amp; DEV TOOLS</text>
      <g transform="translate(0, 20)">
        <!-- React -->
        <g transform="translate(0, 0)">
          <rect x="0" y="0" width="90" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['react']}" fill="#61DAFB" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">React</text>
        </g>
        <!-- Git -->
        <g transform="translate(98, 0)">
          <rect x="0" y="0" width="80" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['git']}" fill="#F05032" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Git</text>
        </g>
        <!-- GitHub -->
        <g transform="translate(186, 0)">
          <rect x="0" y="0" width="95" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['github']}" fill="#f5f7ff" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">GitHub</text>
        </g>
        <!-- Postman -->
        <g transform="translate(289, 0)">
          <rect x="0" y="0" width="95" height="30" rx="6" fill="#101c30" stroke="#23334d" stroke-width="1"/>
          <path d="{ICON_PATHS['postman']}" fill="#FF6C37" transform="translate(8, 7) scale(0.65)"/>
          <text x="30" y="19" fill="#f5f7ff" class="stk-font-mono" font-size="11" font-weight="600">Postman</text>
        </g>
      </g>
    </g>
  </g>
</svg>"""
    return svg


# ==========================================
# 4. BUILD ID-DASHBOARD.SVG
# ==========================================
def build_id_dashboard():
    # Barcode pattern lines
    barcode_bars = ""
    bar_x = 0
    pattern = "101101001011101010010110101001101011010010110101"
    for bit in pattern:
        w = 3 if bit == '1' else 1.5
        barcode_bars += f'<rect x="{bar_x}" y="0" width="{w}" height="28" fill="#f5f7ff" opacity="0.85"/>'
        bar_x += w + 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 440" width="100%" height="100%">
  <defs>
    <style>
{FONT_CSS}
      .idd-font-display {{ font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      .idd-font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}

      /* Drop and Pendulum Swing Animation */
      @keyframes iddDropAndSwing {{
        0% {{ transform: translateY(-70px) rotate(-6deg); }}
        20% {{ transform: translateY(0px) rotate(4deg); }}
        40% {{ transform: translateY(0px) rotate(-3deg); }}
        60% {{ transform: translateY(0px) rotate(2deg); }}
        80% {{ transform: translateY(0px) rotate(-1.7deg); }}
        90% {{ transform: translateY(0px) rotate(1.7deg); }}
        100% {{ transform: translateY(0px) rotate(-1.7deg); }}
      }}

      @keyframes iddContinuousSwing {{
        0% {{ transform: rotate(-1.7deg); }}
        50% {{ transform: rotate(1.7deg); }}
        100% {{ transform: rotate(-1.7deg); }}
      }}

      @keyframes iddFoilSweep {{
        0% {{ transform: translateX(-350px) skewX(-25deg); opacity: 0; }}
        20% {{ opacity: 0.25; }}
        50% {{ transform: translateX(350px) skewX(-25deg); opacity: 0.25; }}
        60%, 100% {{ opacity: 0; }}
      }}

      .idd-card-anim {{
        transform-origin: 165px 45px;
        animation: iddContinuousSwing 6s ease-in-out infinite;
      }}

      .idd-foil-anim {{
        animation: iddFoilSweep 6s infinite ease-in-out;
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <pattern id="idd-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#1b2942" opacity="0.6"/>
    </pattern>

    <linearGradient id="idd-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a101f"/>
      <stop offset="100%" stop-color="#050811"/>
    </linearGradient>

    <linearGradient id="idd-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#23334d" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.4"/>
    </linearGradient>

    <linearGradient id="idd-card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#142138"/>
      <stop offset="100%" stop-color="#0a1220"/>
    </linearGradient>

    <linearGradient id="idd-lanyard-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#1e60cc"/>
      <stop offset="50%" stop-color="#247bff"/>
      <stop offset="100%" stop-color="#154999"/>
    </linearGradient>

    <linearGradient id="idd-metallic-clasp" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="40%" stop-color="#94a3b8"/>
      <stop offset="70%" stop-color="#475569"/>
      <stop offset="100%" stop-color="#cbd5e1"/>
    </linearGradient>

    <linearGradient id="idd-foil-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#247bff" stop-opacity="0.35"/>
      <stop offset="70%" stop-color="#ff354f" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <clipPath id="idd-card-clip">
      <rect x="0" y="0" width="240" height="345" rx="14"/>
    </clipPath>

    <clipPath id="idd-photo-clip">
      <rect x="0" y="0" width="90" height="110" rx="8"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="850" height="440" rx="16" fill="url(#idd-bg-grad)"/>
  <rect x="0" y="0" width="850" height="440" rx="16" fill="url(#idd-dots)"/>
  <rect x="0.5" y="0.5" width="849" height="439" rx="15.5" fill="none" stroke="url(#idd-border-grad)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(40, 36)">
    <rect x="0" y="0" width="8" height="8" rx="2" fill="#247bff"/>
    <text x="18" y="8" fill="#247bff" class="idd-font-mono" font-size="11" font-weight="600" letter-spacing="1.5">SECTION 04 // DEVELOPER ID &amp; VERIFIED DASHBOARD</text>
  </g>

  <!-- ================= LEFT: HANGING LANYARD ID CARD ================= -->
  <!-- Top Anchor & Lanyard Strap -->
  <g transform="translate(165, 0)">
    <!-- Woven Lanyard Strap -->
    <path d="M-12 0 L-10 40 L10 40 L12 0 Z" fill="url(#idd-lanyard-grad)"/>
    <!-- Strap stitch lines -->
    <line x1="-7" y1="0" x2="-6" y2="40" stroke="#f5f7ff" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.6"/>
    <line x1="7" y1="0" x2="6" y2="40" stroke="#f5f7ff" stroke-width="0.8" stroke-dasharray="2,2" opacity="0.6"/>

    <!-- Steel Lobster Clasp / Swivel Ring -->
    <g transform="translate(0, 42)">
      <!-- Swivel Ring -->
      <ellipse cx="0" cy="0" rx="10" ry="5" fill="none" stroke="url(#idd-metallic-clasp)" stroke-width="2.5"/>
      <!-- Metallic Lobster Clasp -->
      <path d="M-5 4 L5 4 L4 18 L-4 18 Z" fill="url(#idd-metallic-clasp)"/>
      <circle cx="0" cy="18" r="4.5" fill="none" stroke="url(#idd-metallic-clasp)" stroke-width="2"/>
    </g>
  </g>

  <!-- Hanging Card Assembly (Pivot: 165, 55) -->
  <g class="idd-card-anim" transform="translate(45, 62)">
    <g clip-path="url(#idd-card-clip)">
      <!-- Card Body -->
      <rect x="0" y="0" width="240" height="345" rx="14" fill="url(#idd-card-grad)"/>
      <rect x="0" y="0" width="240" height="345" rx="14" fill="none" stroke="#247bff" stroke-width="1.2" stroke-opacity="0.4"/>

      <!-- Top Lanyard Hole Punch -->
      <g transform="translate(120, 14)">
        <rect x="-16" y="0" width="32" height="6" rx="3" fill="#070b16" stroke="#23334d" stroke-width="1.2"/>
      </g>

      <!-- Security Foil Sweep Light -->
      <rect x="-100" y="0" width="120" height="350" fill="url(#idd-foil-grad)" class="idd-foil-anim"/>

      <!-- Card Header Banner -->
      <g transform="translate(16, 32)">
        <text x="0" y="10" fill="#247bff" class="idd-font-mono" font-size="8.5" font-weight="700" letter-spacing="1">VERIFIED DEVELOPER ID</text>
        <text x="208" y="10" text-anchor="end" fill="#ff354f" class="idd-font-mono" font-size="8.5" font-weight="700">2026-27</text>
        <line x1="0" y1="16" x2="208" y2="16" stroke="#23334d" stroke-width="1"/>
      </g>

      <!-- Portrait + ID Details Row -->
      <g transform="translate(16, 58)">
        <!-- Photo Container -->
        <g clip-path="url(#idd-photo-clip)">
          <rect x="0" y="0" width="90" height="110" fill="#070b16"/>
          <image href="data:image/png;base64,{id_b64}" x="-10" y="-8" width="110" height="125" preserveAspectRatio="xMidYMid slice"/>
        </g>
        <rect x="0.5" y="0.5" width="89" height="109" rx="7.5" fill="none" stroke="#247bff" stroke-width="1.2" stroke-opacity="0.5"/>

        <!-- Details next to Photo -->
        <g transform="translate(102, 10)">
          <text x="0" y="0" fill="#8995ad" class="idd-font-mono" font-size="8" letter-spacing="0.5">INSTITUTION</text>
          <text x="0" y="13" fill="#f5f7ff" class="idd-font-mono" font-size="9" font-weight="600">REVA UNIV</text>

          <text x="0" y="32" fill="#8995ad" class="idd-font-mono" font-size="8" letter-spacing="0.5">PROGRAM</text>
          <text x="0" y="45" fill="#f5f7ff" class="idd-font-mono" font-size="9" font-weight="600">B.TECH ISE</text>

          <text x="0" y="64" fill="#8995ad" class="idd-font-mono" font-size="8" letter-spacing="0.5">SRN / ID</text>
          <text x="0" y="77" fill="#247bff" class="idd-font-mono" font-size="9" font-weight="700">R25EQ059</text>

          <text x="0" y="96" fill="#00e599" class="idd-font-mono" font-size="8" font-weight="600">● VERIFIED</text>
        </g>
      </g>

      <!-- Name & Role -->
      <g transform="translate(16, 184)">
        <text x="0" y="16" fill="#f5f7ff" class="idd-font-display" font-size="16" font-weight="700">PRASANNA KARAGAR</text>
        <text x="0" y="32" fill="#8995ad" class="idd-font-mono" font-size="9.5" font-weight="600" letter-spacing="0.5">SOFTWARE ENGINEER (IN TRAINING)</text>
      </g>

      <!-- Key Focus Chips -->
      <g transform="translate(16, 230)">
        <rect x="0" y="0" width="98" height="20" rx="4" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <text x="7" y="13" fill="#247bff" class="idd-font-mono" font-size="8.5" font-weight="600">DSA &amp; CP</text>

        <rect x="105" y="0" width="103" height="20" rx="4" fill="#101c30" stroke="#23334d" stroke-width="1"/>
        <text x="7" y="13" fill="#ff354f" class="idd-font-mono" font-size="8.5" font-weight="600">BACKEND ARCH</text>
      </g>

      <!-- Barcode Container -->
      <g transform="translate(16, 268)">
        <rect x="0" y="0" width="208" height="42" rx="6" fill="#080e1a" stroke="#23334d" stroke-width="1"/>
        <g transform="translate(10, 6)">
          {barcode_bars}
        </g>
        <text x="104" y="38" text-anchor="middle" fill="#8995ad" class="idd-font-mono" font-size="7.5" letter-spacing="2">*PK-R25EQ059-REVA*</text>
      </g>
    </g>
  </g>

  <!-- ================= RIGHT: VERIFIED DEVELOPER DASHBOARD ================= -->
  <g transform="translate(325, 60)">
    <!-- Card 1: Academic Track -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="485" height="74" rx="10" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="28" cy="37" r="14" fill="#247bff" fill-opacity="0.15"/>
      <text x="22" y="42" fill="#247bff" font-size="13">🎓</text>
      <text x="54" y="27" fill="#8995ad" class="idd-font-mono" font-size="10" letter-spacing="1">ACADEMIC CREDENTIALS</text>
      <text x="54" y="46" fill="#f5f7ff" class="idd-font-display" font-size="15" font-weight="700">REVA University, Bangalore</text>
      <text x="54" y="63" fill="#247bff" class="idd-font-mono" font-size="11" font-weight="600">B.Tech Information Science Engineering (Class of 2027)</text>
      <rect x="400" y="14" width="70" height="20" rx="4" fill="#080e1a" stroke="#247bff" stroke-width="1"/>
      <text x="435" y="27" text-anchor="middle" fill="#247bff" class="idd-font-mono" font-size="9" font-weight="700">2ND YEAR</text>
    </g>

    <!-- Card 2: Core Engineering Repositories -->
    <g transform="translate(0, 84)">
      <rect x="0" y="0" width="485" height="88" rx="10" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="28" cy="44" r="14" fill="#ff354f" fill-opacity="0.15"/>
      <text x="22" y="49" fill="#ff354f" font-size="13">⚡</text>
      <text x="54" y="24" fill="#8995ad" class="idd-font-mono" font-size="10" letter-spacing="1">FEATURED REPOSITORIES</text>
      
      <!-- Repo 1 -->
      <g transform="translate(54, 34)">
        <text x="0" y="11" fill="#f5f7ff" class="idd-font-mono" font-size="12" font-weight="700">UniRank</text>
        <text x="75" y="11" fill="#8995ad" class="idd-font-mono" font-size="11">— Online Assessment &amp; Code Execution Engine (Judge0/Docker)</text>
      </g>
      <!-- Repo 2 -->
      <g transform="translate(54, 54)">
        <text x="0" y="11" fill="#f5f7ff" class="idd-font-mono" font-size="12" font-weight="700">Exam-Portal</text>
        <text x="100" y="11" fill="#8995ad" class="idd-font-mono" font-size="11">— Scalable Exam Engine &amp; Anti-Cheat Telemetry</text>
      </g>
    </g>

    <!-- Card 3: Competitive Programming & Problem Solving -->
    <g transform="translate(0, 182)">
      <rect x="0" y="0" width="485" height="74" rx="10" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="28" cy="37" r="14" fill="#00e599" fill-opacity="0.15"/>
      <text x="22" y="42" fill="#00e599" font-size="13">🧠</text>
      <text x="54" y="27" fill="#8995ad" class="idd-font-mono" font-size="10" letter-spacing="1">ALGORITHMIC FOCUS &amp; PRACTICE</text>
      <text x="54" y="46" fill="#f5f7ff" class="idd-font-display" font-size="14.5" font-weight="700">LeetCode &amp; Codeforces Active Competitor</text>
      <text x="54" y="63" fill="#8995ad" class="idd-font-mono" font-size="11">Data Structures, Dynamic Programming, Graphs, C++ Optimizations</text>
    </g>

    <!-- Verification / Audit Row at Bottom -->
    <g transform="translate(0, 268)">
      <rect x="0" y="0" width="485" height="52" rx="10" fill="#09111f" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="26" r="4" fill="#00e599"/>
      <text x="36" y="24" fill="#f5f7ff" class="idd-font-mono" font-size="11" font-weight="600">OFFICIAL GITHUB ID: @prasannakaragar</text>
      <text x="36" y="40" fill="#8995ad" class="idd-font-mono" font-size="9.5">VERIFIED REPOSITORY &amp; ACADEMIC DATA // BANGALORE, INDIA</text>
      <rect x="365" y="14" width="105" height="24" rx="5" fill="#101c30" stroke="#00e599" stroke-width="1"/>
      <text x="417" y="29" text-anchor="middle" fill="#00e599" class="idd-font-mono" font-size="9.5" font-weight="700">STATUS: ACTIVE</text>
    </g>
  </g>
</svg>"""
    return svg


# ==========================================
# 5. BUILD CONNECT.SVG
# ==========================================
def build_connect():
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 360" width="100%" height="100%">
  <defs>
    <style>
{FONT_CSS}
      .conn-font-display {{ font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
      .conn-font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace; }}

      /* Character Breathing / Floating Animation */
      @keyframes connCharFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
      }}

      /* Nudging Arrows Animation */
      @keyframes connArrowNudge {{
        0%, 100% {{ transform: translateX(0px); opacity: 0.6; }}
        50% {{ transform: translateX(6px); opacity: 1; }}
      }}

      .conn-char-anim {{
        animation: connCharFloat 4s ease-in-out infinite;
      }}

      .conn-arrow {{
        animation: connArrowNudge 1.8s ease-in-out infinite;
      }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>

    <pattern id="conn-dots" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1" fill="#1b2942" opacity="0.6"/>
    </pattern>

    <linearGradient id="conn-bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a101f"/>
      <stop offset="100%" stop-color="#050811"/>
    </linearGradient>

    <linearGradient id="conn-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#23334d" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ff354f" stop-opacity="0.4"/>
    </linearGradient>

    <radialGradient id="conn-aura-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#247bff" stop-opacity="0.35"/>
      <stop offset="70%" stop-color="#ff354f" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#247bff" stop-opacity="0"/>
    </radialGradient>

    <clipPath id="conn-char-clip">
      <rect x="20" y="10" width="310" height="340" rx="16"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="850" height="360" rx="16" fill="url(#conn-bg-grad)"/>
  <rect x="0" y="0" width="850" height="360" rx="16" fill="url(#conn-dots)"/>
  <rect x="0.5" y="0.5" width="849" height="359" rx="15.5" fill="none" stroke="url(#conn-border-grad)" stroke-width="1.2"/>

  <!-- Section Header -->
  <g transform="translate(40, 36)">
    <rect x="0" y="0" width="8" height="8" rx="2" fill="#247bff"/>
    <text x="18" y="8" fill="#247bff" class="conn-font-mono" font-size="11" font-weight="600" letter-spacing="1.5">SECTION 05 // CONNECT &amp; COLLABORATE</text>
  </g>

  <!-- ================= LEFT: POINTING CHARACTER ================= -->
  <!-- Ambient Character Aura -->
  <circle cx="160" cy="200" r="140" fill="url(#conn-aura-glow)"/>

  <g class="conn-char-anim">
    <!-- Character image placed on left pointing right -->
    <image href="data:image/png;base64,{rp_b64}" x="15" y="25" width="315" height="340" preserveAspectRatio="xMidYMid meet"/>
  </g>

  <!-- ================= RIGHT: GENEROUSLY SPACED SOCIAL CARDS ================= -->
  <g transform="translate(345, 60)">
    <!-- Card 1: LinkedIn -->
    <g transform="translate(0, 0)">
      <rect x="0" y="0" width="465" height="46" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="23" r="13" fill="#0A66C2" fill-opacity="0.2"/>
      <path d="{ICON_PATHS['linkedin']}" fill="#0A66C2" transform="translate(14, 13) scale(0.85)"/>
      <text x="48" y="22" fill="#f5f7ff" class="conn-font-mono" font-size="12" font-weight="600">LinkedIn</text>
      <text x="48" y="36" fill="#8995ad" class="conn-font-mono" font-size="9.5">linkedin.com/in/prasanna-karagar</text>
      <!-- Nudging Arrow -->
      <g class="conn-arrow" transform="translate(425, 23)">
        <path d="M-6 -5 L0 0 L-6 5" fill="none" stroke="#247bff" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- Card 2: LeetCode -->
    <g transform="translate(0, 56)">
      <rect x="0" y="0" width="465" height="46" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="23" r="13" fill="#FFA116" fill-opacity="0.2"/>
      <path d="{ICON_PATHS['leetcode']}" fill="#FFA116" transform="translate(14, 13) scale(0.85)"/>
      <text x="48" y="22" fill="#f5f7ff" class="conn-font-mono" font-size="12" font-weight="600">LeetCode</text>
      <text x="48" y="36" fill="#8995ad" class="conn-font-mono" font-size="9.5">leetcode.com/prasannakaragar</text>
      <g class="conn-arrow" transform="translate(425, 23)">
        <path d="M-6 -5 L0 0 L-6 5" fill="none" stroke="#FFA116" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- Card 3: Codeforces -->
    <g transform="translate(0, 112)">
      <rect x="0" y="0" width="465" height="46" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="23" r="13" fill="#1F8ACB" fill-opacity="0.2"/>
      <path d="{ICON_PATHS['codeforces']}" fill="#1F8ACB" transform="translate(14, 13) scale(0.85)"/>
      <text x="48" y="22" fill="#f5f7ff" class="conn-font-mono" font-size="12" font-weight="600">Codeforces</text>
      <text x="48" y="36" fill="#8995ad" class="conn-font-mono" font-size="9.5">codeforces.com/profile/prasanna_karagar</text>
      <g class="conn-arrow" transform="translate(425, 23)">
        <path d="M-6 -5 L0 0 L-6 5" fill="none" stroke="#1F8ACB" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- Card 4: GitHub -->
    <g transform="translate(0, 168)">
      <rect x="0" y="0" width="465" height="46" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="23" r="13" fill="#f5f7ff" fill-opacity="0.15"/>
      <path d="{ICON_PATHS['github']}" fill="#f5f7ff" transform="translate(14, 13) scale(0.85)"/>
      <text x="48" y="22" fill="#f5f7ff" class="conn-font-mono" font-size="12" font-weight="600">GitHub</text>
      <text x="48" y="36" fill="#8995ad" class="conn-font-mono" font-size="9.5">github.com/prasannakaragar</text>
      <g class="conn-arrow" transform="translate(425, 23)">
        <path d="M-6 -5 L0 0 L-6 5" fill="none" stroke="#f5f7ff" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>

    <!-- Card 5: Direct Email -->
    <g transform="translate(0, 224)">
      <rect x="0" y="0" width="465" height="46" rx="8" fill="#101c30" stroke="#23334d" stroke-width="1"/>
      <circle cx="24" cy="23" r="13" fill="#ff354f" fill-opacity="0.2"/>
      <path d="{ICON_PATHS['mail']}" fill="#ff354f" transform="translate(14, 13) scale(0.85)"/>
      <text x="48" y="22" fill="#f5f7ff" class="conn-font-mono" font-size="12" font-weight="600">Email Inquiries</text>
      <text x="48" y="36" fill="#8995ad" class="conn-font-mono" font-size="9.5">prasannakaragar6@gmail.com</text>
      <g class="conn-arrow" transform="translate(425, 23)">
        <path d="M-6 -5 L0 0 L-6 5" fill="none" stroke="#ff354f" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>
  </g>
</svg>"""
    return svg


# ==========================================
# 6. WRITE SVGS TO ASSETS DIR
# ==========================================
print("Generating SVGs...")
hero_svg = build_hero()
about_svg = build_about()
stack_svg = build_stack()
id_svg = build_id_dashboard()
connect_svg = build_connect()

with open(os.path.join(ASSETS_DIR, 'hero.svg'), 'w', encoding='utf-8') as f:
    f.write(hero_svg)
print(f"Generated hero.svg ({len(hero_svg)} bytes)")

with open(os.path.join(ASSETS_DIR, 'about-life.svg'), 'w', encoding='utf-8') as f:
    f.write(about_svg)
print(f"Generated about-life.svg ({len(about_svg)} bytes)")

with open(os.path.join(ASSETS_DIR, 'stack.svg'), 'w', encoding='utf-8') as f:
    f.write(stack_svg)
print(f"Generated stack.svg ({len(stack_svg)} bytes)")

with open(os.path.join(ASSETS_DIR, 'id-dashboard.svg'), 'w', encoding='utf-8') as f:
    f.write(id_svg)
print(f"Generated id-dashboard.svg ({len(id_svg)} bytes)")

with open(os.path.join(ASSETS_DIR, 'connect.svg'), 'w', encoding='utf-8') as f:
    f.write(connect_svg)
print(f"Generated connect.svg ({len(connect_svg)} bytes)")


# ==========================================
# 7. GENERATE README.MD
# ==========================================
readme_content = """# Hi there, I'm Prasanna Karagar 👋

<div align="center">

![Hero](./assets/hero.svg?v=1)

![About](./assets/about-life.svg?v=1)

![Tech Stack](./assets/stack.svg?v=1)

![Developer ID](./assets/id-dashboard.svg?v=1)

![Connect](./assets/connect.svg?v=1)

</div>

---

### 🌐 Connect With Me

<p align="center">
  <a href="https://linkedin.com/in/prasanna-karagar" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://www.leetcode.com/prasannakaragar" target="_blank">
    <img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=white" alt="LeetCode" />
  </a>
  <a href="https://codeforces.com/profile/prasanna_karagar" target="_blank">
    <img src="https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white" alt="Codeforces" />
  </a>
  <a href="https://github.com/prasannakaragar" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>
  <a href="mailto:prasannakaragar6@gmail.com">
    <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
</p>

---

### 🚀 Featured Engineering Projects

| Project | Description | Tech Stack | Repository |
|:---|:---|:---|:---|
| **UniRank** | High-performance online examination & assessment platform with sandboxed code execution, real-time proctoring telemetry, automated scoring, and LLM integration. | `Node.js` `Express` `React` `Judge0` `Docker` `MySQL` `Supabase` | [prasannakaragar/UniRank](https://github.com/prasannakaragar/UniRank) |
| **Exam-Portal** | Scalable examination portal with role-based access control (RBAC), exam security architecture, and anti-cheat event auditing telemetry. | `Node.js` `Express` `React` `Docker` `Telemetry Audit` | [prasannakaragar/Exam-Portal](https://github.com/prasannakaragar/Exam-Portal) |
| **Academic Portfolio (R25EQ059)** | Modern responsive academic portfolio showcasing architecture, Git collaboration workflows, and static optimization. | `HTML5` `Modern CSS3` `Vanilla JS` `GitHub Pages` | [prasanna-k-2006/R25EQ059](https://github.com/prasanna-k-2006/R25EQ059) |

---

<p align="center">
  <sub>Crafted with precision • Verified REVA University ISE '27 Profile</sub>
</p>
"""

with open(os.path.join(ROOT_DIR, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)
print("Generated README.md")


# ==========================================
# 8. GENERATE PREVIEW.HTML
# ==========================================
preview_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Prasanna Karagar — GitHub Profile Preview</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px 20px;
    }
    .container {
      max-width: 895px;
      width: 100%;
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 6px;
      padding: 32px;
    }
    .section-wrap {
      margin-bottom: 24px;
      display: flex;
      justify-content: center;
    }
    .section-wrap img {
      max-width: 100%;
      height: auto;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    h1 {
      font-size: 26px;
      font-weight: 600;
      margin-bottom: 24px;
      color: #f0f6fc;
      border-bottom: 1px solid #21262d;
      padding-bottom: 12px;
    }
    h2 {
      font-size: 20px;
      color: #f0f6fc;
      margin-top: 32px;
      margin-bottom: 16px;
      border-bottom: 1px solid #21262d;
      padding-bottom: 8px;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
      margin-bottom: 24px;
    }
    th, td {
      border: 1px solid #30363d;
      padding: 10px 14px;
      text-align: left;
      font-size: 14px;
    }
    th {
      background-color: #161b22;
      color: #f0f6fc;
    }
    tr:nth-child(even) {
      background-color: #0d1117;
    }
    tr:nth-child(odd) {
      background-color: #121820;
    }
    a {
      color: #58a6ff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .badges {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      justify-content: center;
      margin: 20px 0;
    }
    .qa-banner {
      background: #161b22;
      border: 1px solid #238636;
      border-radius: 6px;
      padding: 16px 20px;
      margin-bottom: 28px;
      font-size: 13px;
    }
    .qa-banner strong {
      color: #3fb950;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="qa-banner">
      <strong>✓ Playbook Exact Reference Recreation Mode</strong><br>
      Identity: <strong>Prasanna Karagar</strong> (@prasannakaragar) • All 5 SVG sections rendered via <code>&lt;img&gt;</code> elements with transparent assets and embedded fonts.
    </div>

    <h1>Hi there, I'm Prasanna Karagar 👋</h1>

    <!-- 1. HERO -->
    <div class="section-wrap">
      <img src="./assets/hero.svg?v=1" alt="Hero Section">
    </div>

    <!-- 2. ABOUT -->
    <div class="section-wrap">
      <img src="./assets/about-life.svg?v=1" alt="About Section">
    </div>

    <!-- 3. STACK -->
    <div class="section-wrap">
      <img src="./assets/stack.svg?v=1" alt="Tech Stack Section">
    </div>

    <!-- 4. DEVELOPER ID DASHBOARD -->
    <div class="section-wrap">
      <img src="./assets/id-dashboard.svg?v=1" alt="Developer ID Dashboard">
    </div>

    <!-- 5. CONNECT -->
    <div class="section-wrap">
      <img src="./assets/connect.svg?v=1" alt="Connect Section">
    </div>

    <h2>🌐 Connect With Me</h2>
    <div class="badges">
      <a href="https://linkedin.com/in/prasanna-karagar" target="_blank">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
      </a>
      <a href="https://www.leetcode.com/prasannakaragar" target="_blank">
        <img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=white" alt="LeetCode">
      </a>
      <a href="https://codeforces.com/profile/prasanna_karagar" target="_blank">
        <img src="https://img.shields.io/badge/Codeforces-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white" alt="Codeforces">
      </a>
      <a href="https://github.com/prasannakaragar" target="_blank">
        <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
      </a>
      <a href="mailto:prasannakaragar6@gmail.com">
        <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
      </a>
    </div>

    <h2>🚀 Featured Engineering Projects</h2>
    <table>
      <thead>
        <tr>
          <th>Project</th>
          <th>Description</th>
          <th>Tech Stack</th>
          <th>Repository</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>UniRank</strong></td>
          <td>High-performance online examination & assessment platform with sandboxed code execution, real-time proctoring telemetry, automated scoring, and LLM integration.</td>
          <td><code>Node.js</code> <code>Express</code> <code>React</code> <code>Judge0</code> <code>Docker</code> <code>MySQL</code> <code>Supabase</code></td>
          <td><a href="https://github.com/prasannakaragar/UniRank" target="_blank">prasannakaragar/UniRank</a></td>
        </tr>
        <tr>
          <td><strong>Exam-Portal</strong></td>
          <td>Scalable examination portal with role-based access control (RBAC), exam security architecture, and anti-cheat event auditing telemetry.</td>
          <td><code>Node.js</code> <code>Express</code> <code>React</code> <code>Docker</code> <code>Telemetry Audit</code></td>
          <td><a href="https://github.com/prasannakaragar/Exam-Portal" target="_blank">prasannakaragar/Exam-Portal</a></td>
        </tr>
        <tr>
          <td><strong>Academic Portfolio (R25EQ059)</strong></td>
          <td>Modern responsive academic portfolio showcasing architecture, Git collaboration workflows, and static optimization.</td>
          <td><code>HTML5</code> <code>Modern CSS3</code> <code>Vanilla JS</code> <code>GitHub Pages</code></td>
          <td><a href="https://github.com/prasanna-k-2006/R25EQ059" target="_blank">prasanna-k-2006/R25EQ059</a></td>
        </tr>
      </tbody>
    </table>
  </div>
</body>
</html>
"""

with open(os.path.join(ROOT_DIR, 'preview.html'), 'w', encoding='utf-8') as f:
    f.write(preview_html)
print("Generated preview.html")


# ==========================================
# 9. CREATE ZIP PACKAGE
# ==========================================
zip_path = os.path.join(ROOT_DIR, 'github-profile.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add README.md
    zipf.write(os.path.join(ROOT_DIR, 'README.md'), 'README.md')
    # Add preview.html
    zipf.write(os.path.join(ROOT_DIR, 'preview.html'), 'preview.html')
    # Add assets
    for asset_file in os.listdir(ASSETS_DIR):
        asset_full = os.path.join(ASSETS_DIR, asset_file)
        if os.path.isfile(asset_full):
            zipf.write(asset_full, os.path.join('assets', asset_file))
    # Add docs
    for doc_root, _, doc_files in os.walk(os.path.join(ROOT_DIR, 'docs')):
        for df in doc_files:
            rel = os.path.relpath(os.path.join(doc_root, df), ROOT_DIR)
            zipf.write(os.path.join(doc_root, df), rel)

print(f"Created {zip_path} ({os.path.getsize(zip_path)} bytes)")
print("ALL TASKS COMPLETED SUCCESSFULLY!")
