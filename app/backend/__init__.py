from datetime import timedelta
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate

from app.models import db, User, Animal

login_manager = LoginManager()
migrate = Migrate()

# User Loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database."""
    user = User.query.get(int(user_id))
    if user:
        return user
    return None

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

    # Configuration
    app.config['SECRET_KEY'] = 'secret_key_here'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=0)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the extensions with the app instance
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('main.not_logged_in'))

    # Register the blueprint for routes
    from .routes import main
    app.register_blueprint(main)

    return app

# CLI commands
def init_cli_commands(app):
    """Register CLI commands with Flask."""
    from flask.cli import with_appcontext

    @app.cli.command('create-db')
    @with_appcontext
    def create_db():
        """Create the database tables."""
        db.create_all()
        print("Database created!")

    @app.cli.command('seed-db')
    @with_appcontext
    def seed_db():
        """Seed the database with sample data."""
        sample_animal = Animal(
            name="Buddy",
            age=3,
            animal_type="Dog",
            description="Friendly golden retriever",
            image="static/uploads/sample.jpg"
        )
        db.session.add(sample_animal)
        db.session.commit()
        print("Database seeded!")
