from flask import Flask, render_template_string, request

from datetime import datetime

app = Flask(__name__)

# Zodiac signs
RASHIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Nakshatras (27)
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashirsha", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# ---------- HTML Templates (full redesigned UI + animations) ----------
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Numerology Home</title>
  <style>
    :root{
      --bg1: #0f172a; --bg2: #0b1220; --card: #ffffff;
      --accent: #6ee7b7; --blue: #60a5fa; --warm: #fb923c;
      --muted: #94a3b8;
      --glass: rgba(255,255,255,0.06);
    }
    *{box-sizing:border-box}
    body{
      margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
      font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: radial-gradient(1200px 600px at 10% 10%, rgba(96,165,250,0.08), transparent),
                  linear-gradient(135deg, var(--bg1), var(--bg2));
      color: #e6eef8;
    }
    .panel{
      width:920px; max-width:95vw; padding:36px; border-radius:14px;
      background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
      box-shadow: 0 8px 40px rgba(2,6,23,0.6); backdrop-filter: blur(6px);
      display:flex; gap:24px; align-items:center; justify-content:space-between;
      animation: floatIn 600ms ease both;
    }
    @keyframes floatIn { from { transform: translateY(8px); opacity:0 } to { transform: none; opacity:1 } }

    .left {
      flex: 1 1 420px;
    }
    h1{ margin:0; font-size:30px; color:var(--accent) }
    p.lead{ color:var(--muted); margin-top:8px; margin-bottom:22px; }

    .cta {
      display:flex; gap:12px; align-items:center;
    }
    .btn {
      padding:12px 18px; border-radius:10px; font-weight:600; cursor:pointer; border:none;
      color: #081028; background: linear-gradient(90deg,var(--accent), #34d399);
      box-shadow: 0 6px 18px rgba(52,211,153,0.12); transform: translateZ(0);
    }
    .btn.secondary {
      background: transparent; color: var(--accent); border:1px solid rgba(110,231,183,0.12);
      box-shadow:none;
    }

    .right {
      width:420px; max-width:48%;
      display:flex; align-items:center; justify-content:center;
    }
    .preview-card{
      width:100%; border-radius:12px; padding:20px; background:linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.03); text-align:center;
    }
    .preview-icon{ font-size:46px; margin-bottom:6px; }
    .preview-title{ font-size:20px; margin:0; color:#fff }
    .preview-sub{ color:var(--muted); margin-top:6px; }

    @media (max-width:900px){
      .panel{ flex-direction:column; padding:18px }
      .right{ width:100% }
    }

  </style>
</head>
<body>
  <div class="panel">
    <div class="left">
      <h1>🌟 Numerology & Astro Insights</h1>
      <p class="lead">Generate your Lord Planet, Zodiac sign, lucky details, spiritual guide and short predictions instantly.</p>
      <div class="cta">
        <form action="/calculator">
          <button class="btn" type="submit">Open Calculator</button>
        </form>
        <button class="btn secondary" onclick="alert('Tip: Use Day/Month/Year of birth to get accurate results')">How it works</button>
      </div>
    </div>

    <div class="right">
      <div class="preview-card">
        <div class="preview-icon">🔮</div>
        <p class="preview-title">Quick Astro Snapshot</p>
        <p class="preview-sub">Lord Planet • Zodiac • Lucky Number • Gemstone</p>
      </div>
    </div>
  </div>
</body>
</html>
"""

CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Numerology Calculator</title>
  <style>
    :root{
      --bg1:#0b1220; --card:#ffffff; --accent:#60a5fa; --accent2:#f97316;
      --muted:#94a3b8;
    }
    *{box-sizing:border-box}
    body{
      margin:0; min-height:100vh; font-family:Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: linear-gradient(180deg, #071022, #071720); color:#e6eef8;
      display:flex; align-items:center; justify-content:center; padding:32px;
    }

    .wrap{ width:980px; max-width:95vw; display:grid; grid-template-columns: 360px 1fr; gap:28px; align-items:start; }

    .form-card{
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      padding:22px; border-radius:14px; border:1px solid rgba(255,255,255,0.03);
      box-shadow: 0 10px 30px rgba(2,6,23,0.6);
      animation: pop 420ms ease both;
    }
    @keyframes pop { from { transform:translateY(8px); opacity:0 } to { transform:none; opacity:1 } }

    .form-card h2{ margin:0 0 12px 0; color:var(--accent); font-size:20px }
    label{ display:block; color:var(--muted); margin:12px 0 6px; font-size:13px }
    input[type="text"], input[type="number"], input[type="time"]{
      width:100%; padding:10px 12px; border-radius:8px; outline:none; border:1px solid rgba(255,255,255,0.06);
      background: rgba(255,255,255,0.02); color:#e6eef8; font-size:15px;
    }
    .btn-run{
      margin-top:14px; width:100%; padding:12px; border-radius:10px; font-weight:700; border:none;
      background: linear-gradient(90deg, var(--accent), #34d399); color:#041022; cursor:pointer;
      box-shadow: 0 8px 24px rgba(52,211,153,0.08);
    }
    .hint{ font-size:12px; color:var(--muted); margin-top:8px }

    /* result card */
    .result-card{
      padding:20px; border-radius:14px; background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.03); min-height: 320px;
      display:flex; flex-direction:column; gap:16px;
    }
    .profile-top{ display:flex; gap:14px; align-items:center; }
    .big-icon{ font-size:56px; background: rgba(255,255,255,0.02); padding:12px; border-radius:12px; }
    .title-block h3{ margin:0; font-size:18px; color:var(--accent) }
    .sub-muted{ color:var(--muted); margin-top:6px; font-size:13px }

    .detail-grid{ display:grid; grid-template-columns: repeat(2, 1fr); gap:12px; margin-top:8px }
    .detail {
      background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
      padding:12px; border-radius:10px; border:1px solid rgba(255,255,255,0.02);
      transition: transform .18s ease;
    }
    .detail:hover{ transform: translateY(-6px) }
    .detail h4{ margin:0; font-size:14px; color: #fff }
    .detail p{ margin:6px 0 0; color:var(--muted); font-size:13px }

    .big-section{ margin-top:10px; padding:12px; border-radius:10px; background: rgba(255,255,255,0.015); border:1px solid rgba(255,255,255,0.02) }

    .home-btn { margin-top:8px; padding:10px 12px; border-radius:8px; border:none; background:transparent; color:var(--muted); cursor:pointer }

    @media (max-width:980px){
      .wrap{ grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="form-card">
      <h2>🔮 Numerology & Zodiac Calculator</h2>
      <form method="post">
        <label for="name">Name</label>
        <input id="name" name="name" type="text" placeholder="Your name" required>

        <label for="day">Day of Birth</label>
        <input id="day" name="day" type="number" min="1" max="31" required>

        <label for="month">Month of Birth</label>
        <input id="month" name="month" type="number" min="1" max="12" required>

        <label for="year">Year of Birth</label>
        <input id="year" name="year" type="number" min="1900" max="2100" required>

        <label for="time">Time of Birth (HH:MM)</label>
        <input id="time" name="time" type="time" required>

        <label for="place">Place of Birth</label>
        <input id="place" name="place" type="text" placeholder="City, Country" required>

        <label for="lat">Latitude</label>
        <input id="lat" name="lat" type="number" step="0.0001" placeholder="e.g., 28.6139" required>

        <label for="lon">Longitude</label>
        <input id="lon" name="lon" type="number" step="0.0001" placeholder="e.g., 77.2090" required>

        <button class="btn-run" type="submit">Calculate</button>
        <p class="hint">Uses your day/month/year to derive Lord Planet, Zodiac and lucky details.</p>
      </form>
    </div>

    <div class="result-card">
      {% if result %}
      <div class="profile-top">
        <div class="big-icon">{{ planet_icon }}</div>
        <div class="title-block">
          <h3>😎 Lord Planet — {{ lord_planet }}</h3>
          <div class="sub-muted">Lord God: <strong>{{ lord_god }}</strong></div>
          <div class="sub-muted">Welcome, <strong>{{ name }}</strong></div>
        </div>
      </div>

      <div class="detail-grid">
        <div class="detail">
          <h4>Lucky Number</h4>
          <p style="font-size:20px; margin-top:6px;"><strong>{{ lucky_number }}</strong></p>
        </div>
        <div class="detail">
          <h4>Lucky Day</h4>
          <p style="font-size:16px; margin-top:6px;"><strong>{{ lucky_day }}</strong></p>
        </div>
        <div class="detail">
          <h4>Lucky Color</h4>
          <p style="font-size:16px; margin-top:6px;"><strong>{{ lucky_color }}</strong></p>
        </div>
        <div class="detail">
          <h4>Gemstone / Metal</h4>
          <p style="font-size:16px; margin-top:6px;"><strong>{{ gemstone }}</strong><br/><small style="color:var(--muted)">{{ lucky_metal }}</small></p>
        </div>
      </div>

      <div class="big-section">
        <h4>🪐 Zodiac(Surya Rashi) — {{ zodiac }} {{ zodiac_icon }}</h4>
        <p class="sub-muted" style="margin-top:8px;">{{ zodiac_traits }}</p>
      </div>

      <div class="big-section">
        <h4>Place of Birth</h4>
        <p class="sub-muted">{{ place }} (Lat: {{ lat }}, Lon: {{ lon }})</p>
      </div>

      <div class="big-section">
        <h4>Health Prediction</h4>
        <p class="sub-muted">{{ health_prediction }}</p>
      </div>

      <div class="big-section">
        <h4>Career Prediction</h4>
        <p class="sub-muted">{{ career_prediction }}</p>
      </div>

      <div style="display:flex; gap:10px; justify-content:flex-end; margin-top:6px;">
        <form action="/" method="get"><button class="home-btn" type="submit">🏠 Home</button></form>
      </div>

      {% else %}
      <div style="text-align:center; color:var(--muted);">
        <p style="margin:40px 0">Your astro profile will appear here after you calculate.</p>
      </div>
      {% endif %}
    </div>
  </div>
</body>
</html>
"""

# -----------Lucky data extended with metal and lord_god ------
lucky_data = {
    "Sun":     {"number": 1, "color": "Gold",   "gem": "Ruby",           "metal": "Gold",      "lord_god": "Surya (Sun God)"},
    "Moon":    {"number": 2, "color": "White",  "gem": "Pearl",          "metal": "Silver",    "lord_god": "Chandra / Shiva"},
    "Mars":    {"number": 9, "color": "Red",    "gem": "Coral",          "metal": "Copper",    "lord_god": "Mangala (Mars God)"},
    "Mercury": {"number": 5, "color": "Green",  "gem": "Emerald",        "metal": "Mercury-like(Alloy)", "lord_god": "Budha (Mercury God)"},
    "Jupiter": {"number": 3, "color": "Yellow", "gem": "Yellow Sapphire", "metal": "Gold",      "lord_god": "Brihaspati (Jupiter Guru)"},
    "Venus":   {"number": 6, "color": "Pink",   "gem": "Diamond",        "metal": "Silver",    "lord_god": "Shukra (Venus Guru)"},
    "Saturn":  {"number": 8, "color": "Blue",   "gem": "Blue Sapphire",  "metal": "Iron",      "lord_god": "Shani (Saturn)"},
    "Rahu":    {"number": 4, "color": "Black",  "gem": "Gomed (Hessonite)","metal": "Iron/Lead", "lord_god": "Rahu (Shadow Planet)"},
    "Ketu":    {"number": 7, "color": "Brown",  "gem": "Cat's Eye",      "metal": "Bronze",    "lord_god": "Ketu (Shadow Node)"}
}

# ---------- Numerology + Zodiac Logic ----------
planet = ['Sun','Moon','Jupiter','Rahu','Mercury','Venus','Ketu','Saturn','Mars']

traits_dict = {
    'Sun': 'Born Leader, confident, strong personality',
    'Moon': 'Soft-hearted, imaginative, emotionally balanced',
    'Jupiter': 'Wise, spiritual, teacher energy',
    'Rahu': 'Ambitious, unconventional thinker',
    'Mercury': 'Communicator, clever, business-minded',
    'Venus': 'Artistic, romantic, beauty and luxury',
    'Ketu': 'Mysterious, introverted, spiritual depth',
    'Saturn': 'Hardworking, disciplined, patient',
    'Mars': 'Energetic, warrior spirit, competitive'
}

planet_icons = {
    'Sun':'☀️', 'Moon':'🌙', 'Jupiter':'♃', 'Rahu':'☊',
    'Mercury':'☿', 'Venus':'♀️', 'Ketu':'☋',
    'Saturn':'♄', 'Mars':'♂️'
}

# --- Zodiac ranges (custom 15-to-14 system) ---
zodiac_data = [
    ("Aries",       (4, 15), (5, 14), "♈", "Energetic, bold, natural leader"),
    ("Taurus",      (5, 15), (6, 14), "♉", "Patient, stable, reliable"),
    ("Gemini",      (6, 15), (7, 14), "♊", "Smart, playful, good communicator"),
    ("Cancer",      (7, 15), (8, 14), "♋", "Emotional, caring, intuitive"),
    ("Leo",         (8, 15), (9, 14), "♌", "Confident, charismatic, creative"),
    ("Virgo",       (9, 15), (10,14), "♍", "Detail-oriented, analytical, kind"),
    ("Libra",       (10,15), (11,14), "♎", "Balanced, charming, fair-minded"),
    ("Scorpio",     (11,15), (12,14), "♏", "Intense, powerful, mysterious"),
    ("Sagittarius", (12,15), (1, 14), "♐", "Adventurous, philosophical, free"),
    ("Capricorn",   (1, 15), (2, 14), "♑", "Ambitious, disciplined, mature"),
    ("Aquarius",    (2, 15), (3, 14), "♒", "Innovative, independent, unique"),
    ("Pisces",      (3, 15), (4, 14), "♓", "Dreamy, intuitive, artistic")
]

def get_zodiac(day, month):
    for name, start, end, icon, traits in zodiac_data:
        s_month, s_day = start
        e_month, e_day = end
        if (month == s_month and day >= s_day) or (month == e_month and day <= e_day):
            return name, icon, traits
    return "Unknown", "❓", "No traits found"

def sum_to_unit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def number_to_day(num):
    # Map 1..9 to weekdays (1=Sunday)
    mapping = {
        1: "Sunday", 2: "Monday", 3: "Tuesday", 4: "Wednesday",
        5: "Thursday", 6: "Friday", 7: "Saturday", 8: "Saturday",
        9: "Tuesday"
    }
    return mapping.get(num, "Any Day")

def generate_health_prediction(lord, zodiac):
    # Simple templated predictions — short and friendly
    base = {
        "Sun": "Focus on heart and vitality. Short daily walks and sunlight help.",
        "Moon": "Watch your sleep and hydration — calm routines will help mood.",
        "Mars": "Energy is high — channel it into exercise; avoid overexertion.",
        "Mercury": "Mind and nerves benefit from rest; breathe deeply and relax.",
        "Jupiter": "Good digestive health — balanced diet supports growth and energy.",
        "Venus": "Take care of senses — rest and creative activities soothe you.",
        "Saturn": "Bones, joints, and structure need care; steady routines help.",
        "Rahu": "Stress can surface — grounding practices like meditation help.",
        "Ketu": "Inner balance may feel off; gentle detox and rest help."
    }
    z_hint = f" As a {zodiac}, be mindful of stress triggers."
    return base.get(lord, "Maintain a balanced routine and stay hydrated.") + z_hint

def generate_career_prediction(lord, zodiac):
    base = {
        "Sun": "Leadership roles suit you — step forward for visibility in positive way. Always take a right path and stand for right.",
        "Moon": "Supportive and caring roles flourish — teamwork benefits you. Your nurturing nature will help you grow in fields like baby care, day care, Nurse. If you are in any other industry like Software/Police/Military/Professor/Fashion, you will still do good in these industry if you listen your deep mind. You can handle any situation keeping your self calm and composed. Your positive decisions will can heal and help many.  ",
        "Mars": "Competitive fields and sports suit you — act decisively. Show courage in any field you are, always help one who is in need. Never use your power in wrong way, it can lead you to face your destiny in very bad situation. Always help other and do not spend money blindly. You can be great and outstanding if you always stand with right person.   ",
        "Mercury": "Communication, sales, and tech roles are favorable. Communicate in right way, communication is your key, you are good in it, but make sure you communicate correct, do not deceive or fraud using your communication. You can do well in IT/Software industry, marketing and business as well. ",
        "Jupiter": "Teaching, mentoring, and advisory roles bring success. You can be good teacher and mentor to others, but remember never use your skill in wrong path. Always mentor someone without biasness, without favoritism. Do not force your teaching, do not impose on some one. Help someone grow, then you will grow. You can be good leaders, you can be like wise chancellor/or advisor to the king you are serving. Lord Vishnu blesses you if you do not use your wisdom and knowledge to deceive or fraud someone. ",
        "Venus": "Creative, design, and relationship-driven careers shine. Maa Lakshmi will always bless you with money, prosperity and golden opportunity, unless and until you do not miss and misuse it. You can be in industry like, clothing, FMCG, Pharma, IT/Software, Military, Medical, but your role will not be core work or technical work, however you will enjoy the fame and money from those industry. But if do not understand the value of prosperity and fame, money you get, you may lose everything. ",
        "Saturn": "Long-term projects and disciplined careers reward patience. You will earn with hard work, experience, and lot of maturity you will earn in your career. Experience which you will gain with patience and wait and watch attitude. Patience is bitter, but its fruit is sweet. You can be in any industry, but with your patience you will earn a unbreakable achievement. ",
        "Rahu": "Unconventional roles and innovation could bring breakthroughs. You can be rack to rich example, if you know how to control confusion, pride, envy, greed, wrath, sloth, gluttony, and lust. Never disrespect someone, never deceive someone with your achievement, power, money, fame. ",
        "Ketu": "Research, spiritual, or behind-the-scenes roles are favored. If you learn the power of simplicity, spiritual, sensible you will be blessed by Ketu. Your work will be noticed in very unnatural way, in very unexpected way. But Ketu cosmic power always try to keep you hidden and mystic, so always work and practice in silence and show when your aura need you to prove yourself. "
    }
    z_hint = f" Your {zodiac} nature will influence how you pursue opportunities."
    return base.get(lord, "Focus on your strengths and steady progress.") + z_hint

# ---------- Routes ----------
@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = False
    data = {}

    if request.method == "POST":
        try:
            name = request.form.get("name").strip()
            day = int(request.form.get("day"))
            month = int(request.form.get("month"))
            year = int(request.form.get("year"))
            tob = request.form.get("time")
            place = request.form.get("place").strip()
            lat = float(request.form.get("lat"))
            lon = float(request.form.get("lon"))
        except ValueError:
            return "Invalid input. Please ensure day, month, year are integers, time is valid, and latitude/longitude are valid numbers.", 400

        # Numerology
        total = day + month + year
        single_digit = sum_to_unit(total)
        lord = planet[single_digit - 1]

        # Zodiac
        zodiac, zodiac_icon, zodiac_traits = get_zodiac(day, month)

        # Lucky / Gemstone / Metal / Lord God
        lucky = lucky_data.get(lord, {"number": "-", "color": "-", "gem": "-", "metal": "-", "lord_god": "-"})
        lucky_number = lucky["number"]
        lucky_color = lucky["color"]
        gemstone = lucky["gem"]
        lucky_metal = lucky.get("metal", "-")
        lord_god = lucky.get("lord_god", "-")

        # Lucky Day (map number -> weekday)
        lucky_day = number_to_day(lucky_number)

        # Health & Career predictions
        health_prediction = generate_health_prediction(lord, zodiac)
        career_prediction = generate_career_prediction(lord, zodiac)

        data = {
            "name": name,
            "lord_planet": lord,
            "planet_icon": planet_icons.get(lord, "❖"),
            "traits": traits_dict.get(lord, ""),
            "lucky_number": lucky_number,
            "lucky_color": lucky_color,
            "gemstone": gemstone,
            "lucky_metal": lucky_metal,
            "lord_god": lord_god,
            "zodiac": zodiac,
            "zodiac_icon": zodiac_icon,
            "zodiac_traits": zodiac_traits,
            "lucky_day": lucky_day,
            "place": place,
            "lat": lat,
            "lon": lon,
            "health_prediction": health_prediction,
            "career_prediction": career_prediction
        }
        result = True

    return render_template_string(CALCULATOR_HTML, result=result, **data)

if __name__ == "__main__":
    app.run(debug=True)
