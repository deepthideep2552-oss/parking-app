"""
Parking Slot Booking System - a simple Flask web app
used to demonstrate Docker + Jenkins CI/CD.
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)
app.secret_key = "parking-demo-key"

RATE_PER_HOUR = 20  # Rs. per hour


def create_slots():
    """Two levels (A and B) with 8 slots each. Some slots are for bikes."""
    slots = {}
    for level in ("A", "B"):
        for n in range(1, 9):
            slot_id = f"{level}{n}"
            slots[slot_id] = {
                "id": slot_id,
                "type": "Bike" if n > 6 else "Car",
                "booked": False,
                "vehicle": "",
                "owner": "",
                "booked_at": None,
            }
    return slots


slots = create_slots()


def summary():
    total = len(slots)
    booked = sum(1 for s in slots.values() if s["booked"])
    return {"total": total, "booked": booked, "free": total - booked}


@app.route("/")
def index():
    return render_template("index.html", slots=slots.values(), summary=summary(),
                           rate=RATE_PER_HOUR)


@app.route("/book", methods=["POST"])
def book():
    slot_id = request.form.get("slot_id", "").strip().upper()
    vehicle = request.form.get("vehicle", "").strip().upper()
    owner = request.form.get("owner", "").strip()

    slot = slots.get(slot_id)
    if not slot:
        flash(f"Slot {slot_id} does not exist.", "error")
    elif slot["booked"]:
        flash(f"Slot {slot_id} is already booked.", "error")
    elif not vehicle:
        flash("Please enter a vehicle number.", "error")
    elif any(s["vehicle"] == vehicle for s in slots.values() if s["booked"]):
        flash(f"Vehicle {vehicle} is already parked.", "error")
    else:
        slot.update(booked=True, vehicle=vehicle, owner=owner,
                    booked_at=datetime.now().strftime("%d-%m-%Y %H:%M"))
        flash(f"Slot {slot_id} booked for {vehicle}.", "success")
    return redirect(url_for("index"))


@app.route("/release/<slot_id>", methods=["POST"])
def release(slot_id):
    slot = slots.get(slot_id.upper())
    if slot and slot["booked"]:
        booked_at = datetime.strptime(slot["booked_at"], "%d-%m-%Y %H:%M")
        hours = max(1, -(-int((datetime.now() - booked_at).total_seconds()) // 3600))
        flash(f"Slot {slot['id']} released. {slot['vehicle']} parked {hours} hr(s). "
              f"Amount: Rs. {hours * RATE_PER_HOUR}", "success")
        slot.update(booked=False, vehicle="", owner="", booked_at=None)
    return redirect(url_for("index"))


@app.route("/api/slots")
def api_slots():
    return jsonify({"summary": summary(), "slots": list(slots.values())})


@app.route("/health")
def health():
    return jsonify({"status": "UP"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
