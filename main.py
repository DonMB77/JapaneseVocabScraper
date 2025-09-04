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
    translation = db.Column(db.String(300), nullable=False)
    def __repr__(self) -> str:
        return f"Task {self.id}"


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("homepage.html")
    if request.method == "POST":
        try:
            db.user.query.delete()
            db.commit()
        except Exception as e:
            print(e)
        words = data_proccessing_unit.scrape_japanese_words(request.form['url'])
        try:
            for word in words:
                db.session.add(Vocab(readingJapanese=word[0], wordType=word[1], translation=""))
        except Exception as e:
            print(f"{word}: {e}")
        db.session.commit()
        db.session.commit()
        fiveWords = Vocab.query.limit(5).all()
        fiveWordsMeaning = [data_proccessing_unit.get_jisho_translation(vocab.readingJapanese) for vocab in fiveWords]
        fiveWordsList = [[vocab.readingJapanese, vocab.wordType, fiveWordsMeaning[i]] for i, vocab in enumerate(fiveWords)]
        return render_template("homepage.html", words=fiveWordsList, meanings=fiveWordsMeaning)
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)