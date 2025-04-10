from flask import Flask, render_template, request, redirect
import json, os
import string, random

app = Flask(__name__, template_folder="templates", static_folder="static")
STORE_PATH = os.path.join("../shared", "storage.json")

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        tokens = request.form.getlist("token")
        seats = request.form.getlist("seat")
        event = request.form.get("event")
        date = request.form.get("date")

        new_id = generate_id()

        with open(STORE_PATH, "r") as f:
            data = json.load(f)

        data[new_id] = [
            {"token": t, "seat": s, "event": event, "date": date}
            for t, s in zip(tokens, seats)
        ]

        with open(STORE_PATH, "w") as f:
            json.dump(data, f)

        return f"Ticket link: https://mypassdelivery.com/ticket/{new_id}"

    return render_template("form.html")
