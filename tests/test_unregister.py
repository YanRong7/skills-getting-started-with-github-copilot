"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern"""


def test_unregister_successful(client):
    """Test student successfully unregisters from an activity"""
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregister fails when activity doesn't exist"""
    # Arrange
    email = "alex@mergington.edu"
    activity = "Non-Existent Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_student_not_found(client):
    """Test unregister fails when student not in activity"""
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert "not found in activity" in response.json()["detail"]


def test_unregister_then_signup_again(client):
    """Test student can re-signup after unregistering"""
    # Arrange
    email = "removable@mergington.edu"
    activity = "Basketball Team"

    # Act - First signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act - Unregister
    response_unreg = client.delete(f"/activities/{activity}/participants/{email}")
    # Act - Signup again
    response_signup = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response_unreg.status_code == 200
    assert response_signup.status_code == 200

    # Verify in activity
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]


def test_unregister_decreases_participant_count(client):
    """Test that unregister decreases the participant count for an activity"""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act - Get initial count
    response_before = client.get("/activities")
    count_before = len(response_before.json()[activity]["participants"])

    # Act - Unregister
    client.delete(f"/activities/{activity}/participants/{email}")

    # Act - Get new count
    response_after = client.get("/activities")
    count_after = len(response_after.json()[activity]["participants"])

    # Assert
    assert count_after == count_before - 1


def test_unregister_multiple_participants(client):
    """Test that unregistering one participant doesn't affect others"""
    # Arrange
    email_to_remove = "michael@mergington.edu"
    email_to_remain = "daniel@mergington.edu"
    activity = "Chess Club"

    # Act
    client.delete(f"/activities/{activity}/participants/{email_to_remove}")

    # Assert
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity]["participants"]
    assert email_to_remove not in participants
    assert email_to_remain in participants
