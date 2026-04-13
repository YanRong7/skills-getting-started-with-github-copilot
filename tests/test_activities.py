"""Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_get_all_activities(client):
    """Test retrieves all available activities"""
    # Arrange
    expected_activity_count = 9

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert len(response.json()) == expected_activity_count
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_get_activities_structure(client):
    """Test that each activity has required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields"
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_with_participants(client):
    """Test that activities include current participant emails"""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    chess_club = activities["Chess Club"]
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_empty_participant_list(client):
    """Test that newly added activities have empty participant lists"""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    basketball_team = activities["Basketball Team"]
    assert len(basketball_team["participants"]) == 0
    assert basketball_team["max_participants"] == 15
