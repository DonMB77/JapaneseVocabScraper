from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from util import data_proccessing_unit

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///datbase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Vocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    readingJapanese = db.Column(db.String(50), nullable=False)
    wordType = db.Column(db.String(6), nullable=False)
    translation = db.Column(db.String(100), nullable=False)
    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("homepage.html")
    if request.method == "POST":
        words = data_proccessing_unit.scrape_japanese_words(request.form['url'])
        firstFive = words[:5]
        print(firstFive)
        return render_template("homepage.html", words=firstFive)
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)