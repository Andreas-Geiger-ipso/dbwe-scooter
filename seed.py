from flask import Flask, request, redirect, render_template, session
from models import db, User, Scooter, Booking
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# -----------------
# ROUTES
# -----------------

@app.route("/")
def home():
    return redirect("/login")

# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect("/scooters")

    return render_template("login.html")

# SCOOTERS ANZEIGEN
@app.route("/scooters")
def scooters():
    scooters = Scooter.query.all()
    return render_template("scooters.html", scooters=scooters)

# BOOKING STARTEN
@app.route("/start/<int:scooter_id>")
def start_booking(scooter_id):
    if "user_id" not in session:
        return redirect("/login")

    booking = Booking(
        user_id=session["user_id"],
        scooter_id=scooter_id,
        start_time=datetime.now()
    )

    db.session.add(booking)
    db.session.commit()

    return redirect("/scooters")

# BOOKING BEENDEN
@app.route("/stop/<int:booking_id>")
def stop_booking(booking_id):
    booking = Booking.query.get(booking_id)

    booking.end_time = datetime.now()
    booking.price = 5.0  # simple fixpreis

    db.session.commit()

    return redirect("/scooters")

# -----------------

if __name__ == "__main__":
    app.run(debug=True)