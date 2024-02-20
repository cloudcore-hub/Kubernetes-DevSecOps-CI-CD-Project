from app import app, db

with app.app_context():
    # This will create the database file using SQLAlchemy
    db.create_all()
