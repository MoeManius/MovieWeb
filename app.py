from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Movie, UserMovie, Review
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)


# Route to view movie details and its reviews
@app.route('/movie/<int:movie_id>', methods=['GET'])
def view_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return render_template('view_movie.html', movie=movie, reviews=reviews)


# Route to add a review for a movie
@app.route('/movie/<int:movie_id>/add_review', methods=['POST'])
def add_review(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    user_id = 1  # This would come from the logged-in user, assuming user_id is 1 for now
    review_text = request.form['review_text']
    rating = float(request.form['rating'])

    # Add the review to the database
    new_review = Review(user_id=user_id, movie_id=movie_id, review_text=review_text, rating=rating)
    db.session.add(new_review)
    db.session.commit()

    flash('Review added successfully!')
    return redirect(url_for('view_movie', movie_id=movie_id))


# Route to delete a review
@app.route('/movie/<int:movie_id>/delete_review/<int:review_id>', methods=['POST'])
def delete_review(movie_id, review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()

    flash('Review deleted successfully!')
    return redirect(url_for('view_movie', movie_id=movie_id))


# Route to add a movie to a user's favorites
@app.route('/users/<int:user_id>/add_movie/<int:movie_id>', methods=['POST'])
def add_movie_to_user(user_id, movie_id):
    user = User.query.get_or_404(user_id)
    movie = Movie.query.get_or_404(movie_id)

    if movie not in user.movies:
        user.movies.append(movie)
        db.session.commit()
        flash(f'{movie.title} added to your favorite movies!')

    return redirect(url_for('view_user_movies', user_id=user_id))


# Route to view user and their favorite movies
@app.route('/users/<int:user_id>/movies')
def view_user_movies(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('movie_list.html', user=user, movies=user.movies)


if __name__ == '__main__':
    app.run(debug=True)
