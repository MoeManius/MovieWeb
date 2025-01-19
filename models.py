from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Represents a user in the MovieWeb App."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

class Movie(db.Model):
    """Represents a movie associated with a user."""
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return (f"<Movie(id={self.id}, name='{self.name}', director='{self.director}', "
                f"year={self.year}, rating={self.rating}, user_id={self.user_id})>")
