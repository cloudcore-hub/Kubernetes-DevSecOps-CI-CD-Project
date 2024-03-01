import pytest
from app import app
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId

# Mock data for testing
mock_user = {
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "email": "test@example.com",
    "password": generate_password_hash("password"),
    "is_admin": False
}
mock_questions = [
    {"question": "Test Question 1", "correct_answer": "Answer1"},
    {"question": "Test Question 2", "correct_answer": "Answer2"}
]

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF tokens in the forms
    client = app.test_client()

    # Mock MongoDB connection
    with app.app_context():
        app.mongo_client = MongoClient('mongomock://localhost')
        app.mongo_db = app.mongo_client['test_quiz_database']
        app.users_collection = app.mongo_db['users']
        app.questions_collection = app.mongo_db['questions']
        app.scores_collection = app.mongo_db['scores']

        # Insert mock data
        app.users_collection.insert_one(mock_user)
        app.questions_collection.insert_many(mock_questions)

    yield client

    # Clean up the mock data
    with app.app_context():
        app.mongo_client.drop_database('test_quiz_database')

# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

# Test user signup
def test_signup(client):
    response = client.post('/signup', data={'email': 'newuser@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]  # Redirect or success

# Test user login
def test_login(client):
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]

# Test accessing quiz without login
def test_access_quiz_without_login(client):
    response = client.get('/quiz')
    assert response.status_code == 302  # Should redirect to login

# Add more tests as needed
