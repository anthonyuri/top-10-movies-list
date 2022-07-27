from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from movie_api import get_movies

api_key = "af5a744440bd1b9defc86acf28484561"
API_URL = "https://api.themoviedb.org/3/search/movie?"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

class AddForm(FlaskForm):
    new_movie = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")

class EditForm(FlaskForm):
    new_rating = StringField(label='Your Rating Out of 10 e.g. 7.5')
    new_review = StringField(label='Your Review')
    submit = SubmitField(label="Done")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-list.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable= True)
    ranking = db.Column(db.Integer, nullable= True)
    review = db.Column(db.String(250), nullable= True)
    img_url = db.Column(db.String(250), nullable= False)

# db.create_all()

@app.route("/")
def home():
    # movie_list = db.session.query(Movie).all()
    movie_list = Movie.query.order_by(Movie.rating).all()
    movie_list.reverse()
    c = 1
    for movie in movie_list:
        movie.ranking = c
        c += 1

    return render_template("index.html", movies=movie_list)

@app.route("/add", methods=["POST", "GET"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        new_movie = add_form.new_movie.data
        movie_selections = get_movies(new_movie)
        return render_template("select.html", movie_list=movie_selections)
    return render_template("add.html", form=add_form)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    edit_form = EditForm()
    movie_id = request.args.get('id')
    movie_selected = Movie.query.get(movie_id)
    if edit_form.validate_on_submit():
        new_rating = edit_form.new_rating.data
        new_review = edit_form.new_review.data
        movie_selected.rating = new_rating
        movie_selected.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=movie_selected, form=edit_form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}?"
        # The language parameter is optional, if you were making the website for a different audience
        # e.g. Hindi speakers then you might choose "hi-IN"
        response = requests.get(movie_api_url, params={"api_key": api_key, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data['original_title'],
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", id=new_movie.id))


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
