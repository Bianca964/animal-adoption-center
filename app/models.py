from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_login import UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
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



# Route to render the upload page
@app.route('/upload', methods=['POST'])
@login_required
def upload_animal():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        animal_type = request.form['animal_type']
        description = request.form['description']
        image = request.form['image']
        new_animal = Animal(name=name, age=age, animal_type=animal_type, description=description, image=image)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html')



if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)