from flask import Flask, request, render_template, session
import random
import os
import string

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Needed for session

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_special=True, readable=False):
    if readable:
        # Generate a pronounceable password using consonant-vowel patterns
        consonants = "bcdfghjklmnpqrstvwxyz"
        vowels = "aeiou"
        pattern = (consonants, vowels)
        password = ""
        for i in range(length):
            pool = pattern[i % 2]  # Alternate between consonant and vowel
            password += random.choice(pool)
        return password

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
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
    history = session.get("history", [])

    if request.method == "POST":
        length = int(request.form.get("length", 12))
        use_upper = "upper" in request.form
        use_lower = "lower" in request.form
        use_digits = "digits" in request.form
        use_special = "special" in request.form
        readable = "readable" in request.form

        password = generate_password(length, use_upper, use_lower, use_digits, use_special, readable)
        strength = get_strength(password)

        # Update history
        history.insert(0, password)
        history = history[:5]  # Limit to last 5
        session["history"] = history

    return render_template("index.html", password=password, strength=strength, history=history)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)
