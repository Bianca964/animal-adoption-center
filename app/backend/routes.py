import os

from charset_normalizer.utils import is_arabic
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from app.models import db, Animal, User  # Import the Animal model

main = Blueprint('main', __name__)

# --- Mock User Management (Temporary for Testing) ---
# MOCK_ADMIN = {'id': 1, 'username': 'admin', 'password': 'password'}
#
# class User(UserMixin):
#     """A user class compatible with Flask-Login."""
#     def __init__(self, user_id, username):
#         self.id = user_id
#         self.username = username
#
#     def is_active(self):
#         """Returns whether the user is active (always True in this example)."""
#         return True
#
#     def is_anonymous(self):
#         """Returns False as this is not an anonymous user."""
#         return False
#
#     def get_id(self):
#         """Returns the unique ID of the user."""
#         return str(self.id)

# Home Page Route
@main.route('/')
def home():
    """Display animal categories and images."""
    # Fetch categories and animals from the database
    animals = Animal.query.all()
    categories = {}
    for animal in animals:
        categories.setdefault(animal.animal_type, []).append(animal.image)

    return render_template('home.html', categories=categories)

# Login Page Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate admin (replace with real database check later)
        user = User.query.filter_by(username=username).first()
        print(user.password)
        if user and user.check_password(password):
            # user = User(MOCK_ADMIN['id'], MOCK_ADMIN['username'])
            login_user(user, remember=True)
            return redirect(url_for('main.login_successful'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@main.route('/login_successful')
def login_successful():
    """Display login successful page."""
    return render_template('login_successful.html')

# Upload Page Route
@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Handle image uploads."""
    if request.method == 'POST':
        image = request.files['image']
        name = request.form['name']
        age = request.form['age']
        animal_type = request.form['type']
        description = request.form['description']

        if image:
            # Save the image in the appropriate folder
            save_path = os.path.join(current_app.root_path, 'static', 'images', animal_type)
            os.makedirs(save_path, exist_ok=True)
            image_path = os.path.join(save_path, image.filename)
            image.save(image_path)

            # Save the animal to the database
            relative_image_path = os.path.join('static', 'images', animal_type, image.filename)
            animal = Animal(
                name=name,
                age=age,
                animal_type=animal_type,
                description=description,
                image=relative_image_path
            )
            db.session.add(animal)
            db.session.commit()

            flash('Animal uploaded successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('No file selected. Please choose a file to upload.', 'danger')

    return render_template('upload.html')

# About Page Route
@main.route('/about')
def about():
    """Display information about the adoption center."""
    return render_template('about.html')

@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Handle sign up logic here
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('main.sign_up'))

        # Create a new user
        new_user = User(username=username, password=password, email=email, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('main.sign_up_successful'))
    return render_template('sign_up.html')

@main.route('/sign_up_successful')
def sign_up_successful():
    """Display sign up successful page."""
    return render_template('sign_up_successful.html')

@main.route('/log_out_successful')
def log_out_successful():
    """Display log out successful page."""
    return render_template('log_out_successful.html')

# Log Out Route
@main.route('/logout')
def logout():
    """Log out the user."""
    flash('You have been logged out.', 'info')
    logout_user()
    return render_template('log_out_successful.html')


@main.route('/not_logged_in')
def not_logged_in():
    return render_template('not_logged_in.html')
