from flask import Flask, render_template, abort
import json, os
import pdf417gen
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__, template_folder="templates", static_folder="static")
STORE_PATH = os.path.join("../shared", "storage.json")

def generate_barcode_img(token):
    codes = pdf417gen.encode(token, columns=6, security_level=5)
    image = pdf417gen.render_image(codes)  # PIL Image
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

@app.route("/ticket/<ticket_id>")
def ticket(ticket_id):
    with open(STORE_PATH) as f:
        data = json.load(f)

    if ticket_id not in data:
        abort(404)

    pages = [
        {
            **item,
            "barcode": generate_barcode_img(item["token"])
        }
        for item in data[ticket_id]
    ]

    return render_template("ticket.html", pages=pages)
