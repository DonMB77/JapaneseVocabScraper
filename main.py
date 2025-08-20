from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datbase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("homepage.html")
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)