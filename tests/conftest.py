import pytest
from fastapi.testclient import TestClient
import copy
from src.app import app, activities


@pytest.fixture
def client():
    """Provides a TestClient for making requests to the app"""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """Provides a fresh copy of activities data for each test"""
    return copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(clean_activities):
    """Automatically reset activities before each test"""
    # Clear existing activities
    activities.clear()
    # Repopulate with clean data
    activities.update(clean_activities)
    yield
    # Cleanup after test
    activities.clear()
    activities.update(clean_activities)
