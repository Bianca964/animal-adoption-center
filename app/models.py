from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Database model for a user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Animal(db.Model):
    """Database model for an animal."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(20), nullable=False)  # Could use Integer, depending on input
    animal_type = db.Column(db.String(50), nullable=False)  # e.g., "dog", "cat"
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=False)  # Path to the image file

    def __repr__(self):
        return f'<Animal {self.name} ({self.animal_type})>'
