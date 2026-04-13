import pytest
from fastapi.testclient import TestClient
import copy
from src.app import app, activities


# Store original activities state at module import time
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """Provides a TestClient for making requests to the app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Automatically reset activities before and after each test"""
    # Reset before test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
