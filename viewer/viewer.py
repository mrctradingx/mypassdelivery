# viewer/viewer.py
from flask import Flask, render_template
import requests, os

app = Flask(__name__)

@app.route("/booking/<booking_id>")
def show_booking(booking_id):
    api_url = f"https://admin.mypassdelivery.com/api/booking/{booking_id}"
    response = requests.get(api_url)
    if response.status_code != 200:
        return "❌ Booking not found", 404
    tickets = response.json()
    return render_template("ticket.html", tickets=tickets)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
