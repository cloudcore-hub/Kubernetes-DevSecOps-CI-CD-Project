import pytest
from app import app, db, User, Question, Score

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()  # Create a new test database

    yield client

    with app.app_context():
        db.drop_all()  # Clean up the database


# Test the index route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200


# Test user signup
def test_signup(client):
    response = client.post('/signup', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]  # Redirect or success


# Test user login
def test_login(client):
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code in [200, 302]


# Test accessing quiz without login
def test_access_quiz_without_login(client):
    response = client.get('/quiz')
    assert response.status_code == 302  # Should redirect to login


# # Test admin access
# @pytest.mark.parametrize("email, password, status_code", [
#     ('admin@example.com', 'admin', 200),
#     ('user@example.com', 'user', 302),
# ])
# def test_admin_access(client, email, password, status_code):
#     client.post('/login', data={'email': email, 'password': password})
#     response = client.get('/admin')
#     assert response.status_code == status_code

# Add more tests as needed...
