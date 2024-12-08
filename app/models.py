from flask import Flask, jsonify, request, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adoption_center.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

# User model
class User(db.Model, UserMixin):
    """Database model for a user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
    def check_password(self, password):
        """Check if the provided password matches the stored password."""
        return self.password == password

    @property
    def is_active(self):
        """Returns True for active users."""
        return True  # Assuming the user is always active. You can modify this logic later.

# Animal model
class Animal(db.Model):
    """Database model for an animal."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.String(20), nullable=False)  # Age stored as string (e.g., "2 years")
    animal_type = db.Column(db.String(50), nullable=False)  # e.g., "dog", "cat"
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=False)  # Path to the image file

    def __repr__(self):
        return f'<Animal {self.name} ({self.animal_type})>'

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

# Route for the search functionality
@app.route('/search')
def search_animals():
    query = request.args.get('q', '').lower()
    results = Animal.query.filter(Animal.name.ilike(f'%{query}%')).all()
    # Include additional details like type, age, and description in the response
    return jsonify([{
        'name': animal.name,
        'type': animal.animal_type,
        'age': animal.age,
        'description': animal.description,
        'image': animal.image
    } for animal in results])

# Utility route to populate the database with sample data
@app.route('/populate')
def populate_database():
    # Sample data for animals
    sample_animals = [
        {"name": "Lion", "age": "5 years", "animal_type": "Wild", "description": "The king of the jungle", "image": "lion.jpg"},
        {"name": "Tiger", "age": "4 years", "animal_type": "Wild", "description": "A majestic big cat", "image": "tiger.jpg"},
        {"name": "Elephant", "age": "10 years", "animal_type": "Wild", "description": "A gentle giant", "image": "elephant.jpg"},
        {"name": "Bella", "age": "2 years", "animal_type": "Dog", "description": "A friendly and loyal companion", "image": "bella.jpg"},
        {"name": "Kitty", "age": "1 year", "animal_type": "Cat", "description": "Loves to play with yarn", "image": "kitty.jpg"},
    ]
    for animal_data in sample_animals:
        if not Animal.query.filter_by(name=animal_data["name"]).first():
            db.session.add(Animal(**animal_data))
    db.session.commit()
    return "Database populated with sample animals!"

if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)