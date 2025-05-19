from flask import Flask, request, render_template
import random
import os

app = Flask(__name__)

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True):
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    special = "!@#$%^&*()-_=+"

    characters = ""
    if use_upper:
        characters += upper
    if use_lower:
        characters += lower
    if use_digits:
        characters += digits
    if use_special:
        characters += special

    if not characters:
        return ""

    return "".join(random.choice(characters) for _ in range(length))

def get_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+" for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])

    if length >= 12 and score == 4:
        return "Strong"
    elif length >= 8 and score >= 3:
        return "Medium"
    else:
        return "Weak"

@app.route("/", methods=["GET", "POST"])
def index():
    password = ""
    strength = ""
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        use_upper = "upper" in request.form
        use_lower = "lower" in request.form
        use_digits = "digits" in request.form
        use_special = "special" in request.form

        password = generate_password(length, use_upper, use_lower, use_digits, use_special)
        strength = get_strength(password)

    return render_template("index.html", password=password, strength=strength)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
