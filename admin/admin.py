from flask import Flask, render_template, request, redirect, url_for
import json, os, uuid

app = Flask(__name__)
DATA_FILE = "../shared/storage.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        ticket = {
            "event": form["event"],
            "date": form["date"],
            "venue": form["venue"],
            "section": form["section"],
            "row": form["row"],
            "seat": form["seat"],
            "token": form["token"]
        }
        data = load_data()
        ticket_id = str(uuid.uuid4())[:8]
        data[ticket_id] = ticket
        save_data(data)
        return redirect(f"https://mypassticket.onrender.com/ticket/{ticket_id}")
    return render_template("form.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
