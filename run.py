from app.backend import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email='admin@example.com').first()

    # Create the admin user if it doesn't exist
    if not admin:
        admin = User(username='admin', password='admin_password', email='admin@example.com', is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print('Admin user added successfully!')
    else:
        print('Admin user already exists.')
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

