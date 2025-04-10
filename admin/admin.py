from flask import Flask, render_template, request, redirect, jsonify
import os, uuid, json

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
        seats = [s.strip() for s in form["seats"].split(",")]
        tokens = [t.strip() for t in form["tokens"].replace("\r", "").split("\n") if t.strip()]
        
        if len(seats) != len(tokens):
            return "Số ghế và số token không khớp", 400

        booking_id = str(uuid.uuid4())[:8]
        data = load_data()
        for i in range(len(seats)):
            ticket_id = f"{booking_id}_{i+1}"
            data[ticket_id] = {
                "event": form["event"],
                "venue": form["venue"],
                "date": form["date"],
                "section": form["section"],
                "row": form["row"],
                "seat": seats[i],
                "token": tokens[i],
                "booking_id": booking_id
            }
        save_data(data)
        return redirect(f"https://mypassticket.onrender.com/ticket/{booking_id}")
    return render_template("form.html")

@app.route("/api/tickets/<ticket_id>")
def get_ticket_json(ticket_id):
    data = load_data()
    ticket = {k: v for k, v in data.items() if v.get("booking_id") == ticket_id}
    if not ticket:
        return jsonify({"error": "Not found"}), 404
    return jsonify(ticket)
