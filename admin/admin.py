# admin/admin.py
from flask import Flask, render_template, request, redirect
import json, os, uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
        tokens = [t.strip() for t in form["token"].splitlines() if t.strip()]
        seats = [s.strip() for s in form["seat"].split(",") if s.strip()]
        if len(tokens) != len(seats):
            return "❌ Token và ghế phải khớp 1-1", 400
        data = load_data()
        booking_id = str(uuid.uuid4())[:8]
        for token, seat in zip(tokens, seats):
            ticket_id = str(uuid.uuid4())[:8]
            data[ticket_id] = {
                "event": form["event"],
                "date": form["date"],
                "venue": form["venue"],
                "section": form["section"],
                "row": form["row"],
                "seat": seat,
                "token": token,
                "booking_id": booking_id
            }
        save_data(data)
        return redirect(f"https://ticket-viewer-hdvj.onrender.com//booking/{booking_id}")
    return render_template("form.html")

@app.route("/api/tickets/<ticket_id>")
def get_ticket_json(ticket_id):
    data = load_data()
    ticket = data.get(ticket_id)
    if not ticket:
        return {"error": "Not found"}, 404
    return ticket

@app.route("/api/booking/<booking_id>")
def get_booking_json(booking_id):
    data = load_data()
    tickets = [v | {"ticket_id": k} for k, v in data.items() if v.get("booking_id") == booking_id]
    return tickets if tickets else {"error": "Not found"}, 404

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
