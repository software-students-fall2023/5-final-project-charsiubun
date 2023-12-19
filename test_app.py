import os
import pytest
os.environ["TESTING"] = "true"
from app import app as flask_app


@pytest.fixture(name="test_app")
def create_app():
    """Fixture to create a Flask app for testing."""
    app = flask_app
    return app


@pytest.fixture(name="client")
def create_connection(test_app):
    """Fixture to create a test client for the Flask app."""
    return test_app.test_client()


@pytest.fixture(name="database")
def creat_db(test_app):
    with test_app.app_context():
        db = test_app.config["MONGO_CONN"].blog
        db.blogs.insert_one({"owner": "Patrick", "title": "test", "main_body": "test"})
        yield db
        db.blogs.delete_many({})

def test_show_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Login Page</title>" in response.data

def test_show_register(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"<title>Register</title>" in response.data

def test_show_allblogs(client):
    response = client.get("/allblogs/Patrick")
    assert response.status_code == 200
    assert b"<title>All Blog</title>" in response.data

def test_show_addfriend(client):
    response = client.get("/addfriend/Patrick")
    assert response.status_code == 200
    assert b"<title>Add a Friend</title>" in response.data

def test_show_checkout(client):
    response = client.get("/checkout/Patrick")
    assert response.status_code == 200
    assert b"<title>Checkout a Github User!</title>" in response.data

def test_show_myblogs(client):
    response = client.get("/myblogs/Patrick")
    assert response.status_code == 200
    assert b"<title>My Blog</title>" in response.data

def test_show_allblogs_fail(client):
    response = client.get("/allblogs")
    assert response.status_code != 200

def test_show_addfriend_fail(client):
    response = client.get("/addfriend")
    assert response.status_code != 200

def test_show_checkout_fail(client):
    response = client.get("/checkout")
    assert response.status_code != 200

def test_show_myblogs_fail(client):
    response = client.get("/myblogs")
    assert response.status_code != 200

def test_register_fail(client):
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'password123'
    })
    assert response.status_code == 500

def test_login_success(client):
    response = client.post('/', data={
        'username': 'existinguser',
        'password': 'correctpassword'
    })
    assert response.status_code == 200 
    
def test_post_blog(client):
    response = client.post('/myblogs/existinguser', data={
        'title': 'Test Blog',
        'main_body': 'This is a test blog post.'
    })
    assert response.status_code == 302 

def test_add_friend(client):
    response = client.post("/addfriend/testuser", data={'friend': 'frienduser'})
    assert response.status_code == 200 
    assert b"Add a Friend!" in response.data

def test_delete_non_exist_blogpost(client):
    blog_post_id = 'some_id'
    response = client.post("/delete_blogpost", data={'id': blog_post_id, 'owner': 'testuser'})
    assert response.status_code == 500

def test_allnotes_add(client, database):  
    response = client.get(f"/allblogs/Patrick")
    assert response.status_code == 200
    assert b"test" in response.data

def test_delete(client):  
    response = client.post(f"/delete_blogpost")
    assert response.status_code == 400
    