import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from app.models import db, Animal, User  # Import the Animal model

main = Blueprint('main', __name__)

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




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Handle image uploads."""
    if request.method == 'POST':
        image = request.files['image']
        name = request.form.get('name')
        age = request.form.get('age')

        animal_type = request.form.get('type')
        description = request.form.get('description')

        # Validate inputs
        if not all([name, age, animal_type, description, image]):
            flash('All fields are required. Please fill out the form completely.', 'danger')
            return redirect(url_for('main.upload'))

        if not age.isdigit():
            flash('Age must be a number.', 'danger')
            return redirect(url_for('main.upload'))

        if image and allowed_file(image.filename):
            # Save the image
            save_path = os.path.join(current_app.root_path, "static", "images", animal_type)

            os.makedirs(save_path, exist_ok=True)
            image_path = os.path.join(save_path, image.filename)
            image.save(image_path)

            # Save the animal to the database
            relative_image_path = os.path.join("static", "images", animal_type, image.filename)
            animal = Animal(
                name=name,
                age=int(age),
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
    query = request.args.get('q', '').lower()
    results = Animal.query.filter(Animal.name.ilike(f'%{query}%')).all()
    return render_template('animal_search_result.html', animals=results, query=query)



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


@main.route('/animals', methods=['GET'])
def animals():
    animal_type = request.args.get('type')
    if animal_type:
        animals = Animal.query.filter_by(animal_type=animal_type).all()
    else:
        animals = Animal.query.all()
    print (animals)
    return render_template('animals.html', animals=animals, filter_type=animal_type)




@main.route('/delete_animal/<int:animal_id>', methods=['POST'])
@login_required
def delete_animal(animal_id):
    animal = Animal.query.get_or_404(animal_id)
    if current_user.is_admin:  # Ensure only admins can delete
        db.session.delete(animal)
        db.session.commit()
        flash('Animal deleted successfully.', 'success')
    else:
        flash('You do not have permission to perform this action.', 'danger')
    return redirect(url_for('main.animals'))





@main.route('/edit_animal/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def edit_animal(animal_id):
    """Edit an animal's details."""
    animal = Animal.query.get_or_404(animal_id)
    if not current_user.is_admin:
        flash('You do not have permission to perform this action.', 'danger')
        return redirect(url_for('main.animals'))

    if request.method == 'POST':
        animal.name = request.form.get('name', animal.name)
        animal.age = request.form.get('age', animal.age)
        animal.animal_type = request.form.get('type', animal.animal_type)
        animal.description = request.form.get('description', animal.description)

        db.session.commit()
        flash('Animal details updated successfully.', 'success')
        return redirect(url_for('main.animals'))

    return render_template('edit_animal.html', animal=animal)




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
