"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""


def test_signup_successful(client):
    """Test student successfully signs up for an activity"""
    # Arrange
    email = "alex@mergington.edu"
    activity = "Basketball Team"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    # Verify participant was added
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_signup_activity_not_found(client):
    """Test signup fails when activity doesn't exist"""
    # Arrange
    email = "alex@mergington.edu"
    activity = "Non-Existent Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_duplicate_email(client):
    """Test signup fails when student already registered"""
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_multiple_activities(client):
    """Test student can sign up for multiple different activities"""
    # Arrange
    email = "taylor@mergington.edu"

    # Act - Sign up for first activity
    response1 = client.post(f"/activities/Chess Club/signup?email={email}")
    # Act - Sign up for second activity
    response2 = client.post(f"/activities/Art Studio/signup?email={email}")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Verify in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Chess Club"]["participants"]
    assert email in activities["Art Studio"]["participants"]


def test_signup_increases_participant_count(client):
    """Test that signup increases the participant count for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Tennis Club"

    # Act - Get initial count
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity]["participants"])

    # Act - Sign up
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act - Get new count
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity]["participants"])

    # Assert
    assert count_after == count_before + 1
