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

class SavedVocab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    readingJapanese = db.Column(db.String(50), nullable=False)
    wordType = db.Column(db.String(6), nullable=False)
    translation = db.Column(db.String(300), nullable=False)
    def __repr__(self) -> str:
        return f"Task {self.id}"
    
@app.route("/save_vocab", methods=["POST"])
def save_vocab():
    readingJapanese = request.form.get("readingJapanese")
    wordType = request.form.get("wordType")
    translation = request.form.get("translation")
    if readingJapanese and wordType and translation is not None:
        db.session.add(SavedVocab(
            readingJapanese=readingJapanese,
            wordType=wordType,
            translation=translation
        ))
        db.session.commit()
    page = int(request.form.get("page", 0))
    return redirect(f"/?page={page}")

@app.route("/clear", methods=["POST"])
def clear():
    Vocab.query.delete()
    db.session.commit()
    return redirect("/")

@app.route("/", methods=["POST", "GET"])
def index():
    page = int(request.args.get("page", 0))
    per_page = 5
    if request.method == "GET":
        words = Vocab.query.offset(page * per_page).limit(per_page).all()
        for vocab in words:
            if not vocab.translation:
                translation = data_proccessing_unit.get_jisho_translation(vocab.readingJapanese)
                if isinstance(translation, list):
                    translation = "; ".join(translation)
                else:
                    translation = "list conversion error"
                vocab.translation = translation
                db.session.commit()
        next_page = page + 1
        prev_page = page - 1
        return render_template("homepage.html", words=words, next_page=next_page, prev_page=prev_page)
    if request.method == "POST":
        words = data_proccessing_unit.scrape_japanese_words(request.form['url'])
        try:
            for word in words:
                db.session.add(Vocab(readingJapanese=word[0], wordType=word[1], translation=""))
        except Exception as e:
            print(f"{word}: {e}")
        db.session.commit()
        fiveWords = Vocab.query.limit(5).all()
        # Translate and update only if translation is missing
        for vocab in fiveWords:
            if not vocab.translation:
                translation = data_proccessing_unit.get_jisho_translation(vocab.readingJapanese)
                if isinstance(translation, list):
                    translation = "; ".join(translation)
                else:
                    translation = "list conversion error"
                vocab.translation = translation
                db.session.commit()
        next_page = 1
        prev_page = 0
        return render_template("homepage.html", words=fiveWords, next_page=next_page, prev_page=prev_page)
    
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)