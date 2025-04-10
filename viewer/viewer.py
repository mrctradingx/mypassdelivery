from flask import Flask, render_template, send_file
import json, os
import pdf417gen
from PIL import Image

app = Flask(__name__)
DATA_FILE = "../shared/storage.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    data = load_data()
    ticket = data.get(ticket_id)
    if not ticket:
        return "Ticket not found", 404
    return render_template("ticket.html", ticket=ticket, ticket_id=ticket_id)

@app.route("/barcode/<ticket_id>.png")
def barcode(ticket_id):
    data = load_data()
    ticket = data.get(ticket_id)
    if not ticket:
        return "Not found", 404
    code = pdf417gen.encode(ticket["token"])
    image = pdf417gen.render_image(code, scale=3)
    path = f"/tmp/{ticket_id}.png"
    image.save(path)
    return send_file(path, mimetype="image/png")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
