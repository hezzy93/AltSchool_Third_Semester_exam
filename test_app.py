import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Base, get_db

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient


from database import Base, get_db
from main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///"

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread": False}, 
                       poolclass=StaticPool,)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# @pytest.fixture(scope="module")
# def setup_database():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.drop_all(bind=engine)  # Drop all tables
    Base.metadata.create_all(bind=engine)  # Recreate all tables
    yield
    Base.metadata.drop_all(bind=engine)  # Clean up after tests


@pytest.mark.parametrize("last_name, first_name, user_name, email, sex, password", [
    ("testlast_name", "testfirst_name", "testuser_name", "testemail", "testsex", "testpassword")
    ])

def test_signup(client, setup_database, last_name, first_name, user_name, email, sex, password):
    response = client.post("/users_Signup/", json={
        "last_name": last_name, 
        "first_name": first_name,  
        "user_name": user_name,
        "email": email,
        "sex": sex, 
        "password": password
        })

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["user_name"] == user_name
    assert data["user"]["email"] == email


@pytest.mark.parametrize("last_name, first_name, user_name, email, sex, password", [
    ("testlast_name", "testfirst_name", "testuser_name", "testemail", "testsex", "testpassword")
    ])
def test_login(client, setup_database, last_name, first_name, user_name, email, sex, password):
    response = client.post("/users_Signup/", json={
        "last_name": last_name, 
        "first_name": first_name,  
        "user_name": user_name,
        "email": email,
        "sex": sex, 
        "password": password
        })

    # Print the response detail to help diagnose the issue
    print(response.json())  # This will print the error message
    assert response.status_code == 200

    # Then, log in the user
    response = client.post("/users_Login/", data={"username": user_name, "password": password})  # Change to 'username'
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
