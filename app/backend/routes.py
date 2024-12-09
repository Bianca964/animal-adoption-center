import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Animal, User

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
main = Blueprint('main', __name__)

# Home Page Route
@main.route('/')
def home():
    """Display the home page."""
    # Fetch categories and animals from the database
    animals = Animal.query.all()
    categories = {}
    for animal in animals:
        categories.setdefault(animal.animal_type, []).append(animal.image)

    return render_template('home.html', categories=categories)

# Login Page Route
@main.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user and admin login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists and the password is correct and log in the user
        user = User.query.filter_by(username=username).first()
        print(user.password)
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('main.login_successful'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Login Successful Page Route
@main.route('/login_successful')
def login_successful():
    """Display login successful page."""
    return render_template('login_successful.html')

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload Page Route
@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Handle pet uploads."""
    if request.method == 'POST':
        # Request the pet's data and image
        image = request.files['image']
        name = request.form.get('name')
        age = request.form.get('age')

        animal_type = request.form.get('type')
        description = request.form.get('description')

        # Validate the data entered by the user
        if not all([name, age, animal_type, description, image]):
            flash('All fields are required. Please fill out the form completely.', 'danger')
            return redirect(url_for('main.upload'))

        # Check if the age is a number (float) and return an error if not
        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        if not is_float(age):
            flash('Age must be a number.', 'danger')
            return redirect(url_for('main.upload'))

        # Check if the image is valid and save it
        if image and allowed_file(image.filename):
            # Save the image
            save_path = os.path.join(current_app.root_path,"..",  "frontend", "static", "images", animal_type)

            os.makedirs(save_path, exist_ok=True)
            image_path = os.path.join(save_path, image.filename)
            image.save(image_path)

            # Save the animal to the database
            relative_image_path = os.path.join("images", animal_type, image.filename)

            # Create a new animal object and add it to the database
            animal = Animal(
                name=name,
                age=float(age),
                animal_type=animal_type,
                description=description,
                image=relative_image_path
            )
            db.session.add(animal)
            db.session.commit()

            flash('Animal uploaded successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid file type. Please upload an image file (png, jpg, jpeg, gif).', 'danger')

    return render_template('upload.html')


# Route for the search functionality
@main.route('/search')
def search_animals():
    # Get the search query from the URL and convert it to lowercase
    query = request.args.get('q', '').lower()

    # Search the database for animals that match the query
    results = Animal.query.filter(Animal.animal_type.ilike(f'%{query}%')).all()
    return render_template('animal_search_result.html', animals=results, query=query)

# About Page Route
@main.route('/about')
def about():
    """Display information about the adoption center."""
    return render_template('about.html')

# Sign Up Page Route
@main.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Sign up a new user."""
    if request.method == 'POST':
        # Get the user's data from the form
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

# Sign Up Successful Page Route
@main.route('/sign_up_successful')
def sign_up_successful():
    """Display sign up successful page."""
    return render_template('sign_up_successful.html')

# Log Out Successful Page Route
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

# Animals Page Route
@main.route('/animals', methods=['GET'])
def animals():
    """ Display all animals or filter by type."""
    # Get the filter type from the URL
    animal_type = request.args.get('type')

    # Query the database based on the filter type
    if animal_type:
        animals = Animal.query.filter_by(animal_type=animal_type).all()
    else:
        animals = Animal.query.all()

    # Add the `image_path` to each animal
    for animal in animals:
        animal.image_path = f'{animal.image}'

    return render_template('animals.html', animals=animals, filter_type=animal_type)

# Delete Animal Route
@main.route('/delete_animal/<int:animal_id>', methods=['POST'])
@login_required
def delete_animal(animal_id):
    """Delete an animal from the database."""
    animal = Animal.query.get_or_404(animal_id)

    # Check if the user is an admin before deleting the animal
    if current_user.is_admin:
        db.session.delete(animal)
        db.session.commit()
        flash('Animal deleted successfully.', 'success')
    else:
        flash('You do not have permission to perform this action.', 'danger')
    return redirect(url_for('main.animals'))

# Edit Animal Route
@main.route('/edit_animal/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def edit_animal(animal_id):
    """Edit an animal's details."""
    animal = Animal.query.get_or_404(animal_id)
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.animals'))

    if request.method == 'POST':
        # Update the animal's details
        animal.name = request.form.get('name', animal.name)
        animal.age = request.form.get('age', animal.age)
        animal.animal_type = request.form.get('type', animal.animal_type)
        animal.description = request.form.get('description', animal.description)

        db.session.commit()
        flash('Animal details updated successfully.', 'success')
        return redirect(url_for('main.animals'))

    return render_template('edit_animal.html', animal=animal)

# Adopt Animal Route
@main.route('/adopt/<int:animal_id>', methods=['GET', 'POST'])
def adopt_animal(animal_id):
    if not current_user.is_authenticated:
        # Redirect the user to the login page if they are not logged in
        flash('You must be logged in to adopt an animal.', 'warning')
        return redirect(url_for('main.not_logged_in'))

    animal = Animal.query.get_or_404(animal_id)
    if request.method == 'POST':
        # Get the adopter's information from the form
        adopter_name = request.form.get('adopter_name')
        adopter_email = request.form.get('adopter_email')
        adopter_phone = request.form.get('adopter_phone')
        adopter_address = request.form.get('adopter_address')

        db.session.delete(animal)
        db.session.commit()

        flash(f'You have successfully applied to adopt {animal.name}!', 'success')
        return redirect(url_for('main.animals'))
    return render_template('adopt_form.html', animal=animal)

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
