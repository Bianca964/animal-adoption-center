import os
from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user, UserMixin

main = Blueprint('main', __name__)

# --- Mock User Management (Temporary for Testing) ---
# Replace this later with database integration or a user model
MOCK_ADMIN = {'id': 1, 'username': 'admin', 'password': 'password'}

class User(UserMixin):
    """A user class compatible with Flask-Login."""
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

    def is_active(self):
        """Returns whether the user is active (always True in this example)."""
        return True

    def is_anonymous(self):
        """Returns False as this is not an anonymous user."""
        return False

    def get_id(self):
        """Returns the unique ID of the user."""
        return str(self.id)


# Home Page Route
@main.route('/')
def home():
    """Display animal categories and images."""
    # Mock categories and images (replace with real data later)
    categories = {
        'dogs': ['dog1.jpg', 'dog2.jpg'],
        'cats': ['cat1.jpg', 'cat2.jpg']
    }
    return render_template('home.html', categories=categories)

# Login Page Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Handle admin login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate admin (replace with real database check later)
        if username == MOCK_ADMIN['username'] and password == MOCK_ADMIN['password']:
            user = User(MOCK_ADMIN['id'], MOCK_ADMIN['username'])
            login_user(user, remember=True)
            # user.is_authenticated = True
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
            image.save(os.path.join(save_path, image.filename))

            flash('Image uploaded successfully!', 'success')
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
        return redirect(url_for('main.sign_up_successful'))
    return render_template('sign_up.html')


@main.route('/sign_up_successful')
def sign_up_successful():
    """Display login successful page."""
    return render_template('sign_up_successful.html')

@main.route('/log_out_successful')
def log_out_successful():
    """Display login successful page."""
    return render_template('log_out_successful.html')

# Log Out Route
@main.route('/logout')
def logout():
    # Handle log out logic here
    flash('You have been logged out.', 'info')
    logout_user()
    return render_template('log_out_successful.html')