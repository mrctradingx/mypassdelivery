# viewer/viewer.py
from flask import Flask, render_template, send_file, request
import requests, io
import pdf417gen
from PIL import Image
import os

app = Flask(__name__)

ADMIN_API = os.environ.get("ADMIN_API", "https://admin.mypassdelivery.com")

@app.route("/ticket/<ticket_id>")
def show_ticket(ticket_id):
    index = int(request.args.get("index", 0))
    # Call API from admin
    try:
        res = requests.get(f"{ADMIN_API}/api/tickets/{ticket_id}")
        data = res.json()
    except Exception:
        return "Error fetching ticket", 500

    if "tokens" not in data or index >= len(data["tokens"]):
        return "Not Found", 404

    ticket = {
        "event": data.get("event", ""),
        "venue": data.get("venue", ""),
        "date": data.get("date", ""),
        "section": data.get("section", ""),
        "row": data.get("row", ""),
        "seat": data.get("seats")[index],
        "token": data["tokens"][index]
    }

    return render_template("ticket.html", ticket=ticket, ticket_id=ticket_id, index=index, total=len(data["tokens"]))

@app.route("/barcode/<ticket_id>")
def generate_barcode(ticket_id):
    index = int(request.args.get("index", 0))
    try:
        res = requests.get(f"{ADMIN_API}/api/tickets/{ticket_id}")
        data = res.json()
        raw_token = data["tokens"][index]
    except Exception:
        return "Bad token", 400

    codes = pdf417gen.encode(raw_token, columns=6, security_level=5)
    image = pdf417gen.render_image(codes)  # PIL image
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
