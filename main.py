from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# set the Flask app
app = Flask(__name__)

# Config sql database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(app)

# create the model of the database
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    review = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"{self.title} - {self.author} - {self.review}"


db.create_all()

# render the home page
@app.route('/', methods=["POST", "GET"])
def home():
    books = Books.query.all()
    len_book = len(books)
    return render_template("index.html",len_book=len_book, books=books)

# create the delete function and route
@app.route('/delete/<string:ids>')
def delete(ids):
    book_id = ids
    book_to_delete = Books.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# create the add functio and route
@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        title = request.form.get("name")
        author = request.form.get("author")
        rating = request.form.get("rating")
        book1 = Books(title=f'{title}', author=f'{author}', review=f'{rating}/10')
        db.session.add(book1)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

# create the edit function and route
@app.route('/edit/<string:ids>', methods=["POST", "GET"])
def edit(ids):
    if request.method == "POST":
        new_rating = request.form.get("new_rating")
        book_id = ids
        book_to_update = Books.query.get(book_id)
        book_to_update.review = f"{new_rating}/10"
        db.session.commit()
        return redirect(url_for('home'))
    current_rating = Books.query.filter_by(id=ids).first()
    return render_template("edit.html", book_title=current_rating)

# start the server
if __name__ == "__main__":
    app.run(debug=True)
