import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

# --- Mock User Management (Temporary for Testing) ---
# Replace this later with database integration or a user model
MOCK_ADMIN = {'id': 1, 'username': 'admin', 'password': 'password'}

class User:
    """A simple user class for Flask-Login compatibility."""
    def __init__(self, user_id):
        self.id = user_id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
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
            user = User(MOCK_ADMIN['id'])
            login_user(user)
            return redirect(url_for('main.login_successful'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@main.route('/login_successful')
def login_successful():
    """Display login successful page."""
    return render_template('login_successful.html')

# Logout Route
@main.route('/logout')
@login_required
def logout():
    """Log the admin out."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

# Upload Page Route
@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Handle image uploads."""
    if request.method == 'POST':
        image = request.files['file']
        category = request.form['category']

        if image:
            # Save the image in the appropriate folder
            save_path = os.path.join(current_app.root_path, 'static', 'images', category)
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
