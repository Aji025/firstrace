from flask import Flask, render_template_string, request

app = Flask(__name__)

# ---------- Home Page ----------
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home Page</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 60px; background-color: #f0f4f8; }
        .button { padding: 15px 25px; font-size: 20px; border-radius: 8px; border: none; background-color: #3182ce; color: white; cursor: pointer; }
        .button:hover { background-color: #2b6cb0; }
    </style>
</head>
<body>
    <h1>🌟 Welcome to Numerology App</h1>
    <p>Click below to go to the Lord Planet Calculator</p>
    <form action="/calculator">
        <button class="button" type="submit">Go to Calculator</button>
    </form>
</body>
</html>
"""

# ---------- Calculator Page (from htmlpage.py) ----------
CALCULATOR_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Numerology Lord Planet</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin: 40px; background-color: #f0f4f8; }
        form { background-color: white; padding: 25px; display: inline-block; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        input, button { margin: 8px; padding: 8px 12px; font-size: 16px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #3182ce; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #2b6cb0; }
        .card {
            margin-top: 25px;
            display: inline-block;
            padding: 20px;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            min-width: 250px;
        }
        .planet-icon { font-size: 48px; margin-bottom: 10px; }
        .planet-name { font-size: 24px; font-weight: bold; color: #2b6cb0; }
        .traits { font-size: 18px; margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🔮 Numerology Lord Planet Calculator</h1>
    <form method="post">
        <input type="text" name="name" placeholder="Enter your name" required><br>
        <input type="number" name="day" placeholder="Day of Birth" min="1" max="31" required><br>
        <input type="number" name="month" placeholder="Month of Birth" min="1" max="12" required><br>
        <input type="number" name="year" placeholder="Year of Birth" min="1900" max="2100" required><br>
        <button type="submit">Calculate</button>
    </form>

    {% if result %}
    <div class="card">
        <div class="planet-icon">{{ planet_icon }}</div>
        <p class="planet-name">{{ lord_planet }}</p>
        <p class="traits">{{ traits }}</p>
        <p>Welcome <b>{{ name }}</b>! 🎉</p>
    </div>
    {% endif %}
    <!-- Home button -->
    <form action="/" method="get">
        <button class="home-btn" type="submit">🏠 Home</button>
    </form>
</body>
</html>
"""

# ---------- Numerology Logic ----------
planet = ['Sun','Moon','Jupitor','Rahu','Mercury','Venus','Ketu','Saturn','Mars']
traits_dict = {
    'Sun':'Born Leader',
    'Moon':'Kind Hearted',
    'Jupitor':'Wisdom and Guru',
    'Rahu':'Obsessed with everything',
    'Mercury':'Communicator and Business minded',
    'Venus':'Artistic',
    'Ketu':'Secret keeper and mysterious',
    'Saturn':'Hardworker and stubborn',
    'Mars':'Fighter and sporty'
}
planet_icons = {
    'Sun':'☀️', 'Moon':'🌙', 'Jupitor':'♃', 'Rahu':'☊', 'Mercury':'☿',
    'Venus':'♀️', 'Ketu':'☋', 'Saturn':'♄', 'Mars':'♂️'
}

def sum_to_unit(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

# ---------- Flask Routes ----------
@app.route("/")
def home():
    return render_template_string(HOME_HTML)

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    name = day = month = year = lord_planet = traits = planet_icon = None

    if request.method == "POST":
        name = request.form.get("name").strip()
        day = int(request.form.get("day"))
        month = int(request.form.get("month"))
        year = int(request.form.get("year"))

        numday = day + month + year
        single_digit = sum_to_unit(numday)
        lord_planet = planet[single_digit - 1]
        traits = traits_dict[lord_planet]
        planet_icon = planet_icons[lord_planet]

        result = True

    return render_template_string(CALCULATOR_HTML, result=result, name=name,
                                  lord_planet=lord_planet, traits=traits,
                                  planet_icon=planet_icon)

if __name__ == "__main__":
    app.run(debug=True)
