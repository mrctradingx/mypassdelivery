# admin/admin.py
from flask import Flask, render_template, request, redirect, jsonify
import json, os, uuid

app = Flask(__name__)
DATA_FILE = "../shared/storage.json"

def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form = request.form
        seats = form["seats"].split(",")  # multiple seats
        tokens = form["tokens"].split(",")  # 1-to-1 with seats
        if len(seats) != len(tokens):
            return "Seats and tokens count mismatch", 400

        ticket_id = str(uuid.uuid4())[:8]
        ticket = {
            "event": form["event"],
            "date": form["date"],
            "venue": form["venue"],
            "section": form["section"],
            "row": form["row"],
            "seats": seats,
            "tokens": tokens
        }

        data = load_data()
        data[ticket_id] = ticket
        save_data(data)
        return redirect(f"https://mypassticket.onrender.com/ticket/{ticket_id}")
    return render_template("form.html")

@app.route("/api/tickets/<ticket_id>")
def get_ticket_json(ticket_id):
    data = load_data()
    ticket = data.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ticket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
