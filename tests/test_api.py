import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestActivitiesAPI:
    """Test cases for the Activities API endpoints"""

    def test_get_activities(self, client: TestClient):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) == 5  # We have 5 activities defined

        # Check that all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Debate Club", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in activities

        # Check structure of an activity
        chess_club = activities["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_signup_successful(self, client: TestClient):
        """Test successful signup for an activity"""
        activity_name = "Debate Club"
        email = "test@student.edu"

        # Initially, Debate Club should have no participants
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

        # Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the student was added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client: TestClient):
        """Test signup for non-existent activity"""
        response = client.post(
            "/activities/NonExistentActivity/signup",
            params={"email": "test@student.edu"}
        )
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_signed_up(self, client: TestClient):
        """Test signup when student is already signed up"""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # This email is already in Chess Club

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_duplicate_after_signup(self, client: TestClient):
        """Test duplicate signup after successful signup"""
        activity_name = "Science Club"
        email = "new@student.edu"

        # First signup should succeed
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Second signup should fail
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

        data = response.json()
        assert "already signed up" in data["detail"]

    def test_delete_signup_successful(self, client: TestClient):
        """Test successful deletion of signup"""
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # This email is already signed up

        # Verify initially signed up
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

        # Delete signup
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the student was removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_delete_signup_activity_not_found(self, client: TestClient):
        """Test delete signup for non-existent activity"""
        response = client.delete(
            "/activities/NonExistentActivity/signup",
            params={"email": "test@student.edu"}
        )
        assert response.status_code == 404

        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_delete_signup_not_signed_up(self, client: TestClient):
        """Test delete signup when student is not signed up"""
        activity_name = "Debate Club"
        email = "notsignedup@student.edu"

        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

        data = response.json()
        assert "not signed up" in data["detail"]

    def test_root_redirect(self, client: TestClient):
        """Test root endpoint redirects to static index"""
        # TestClient follows redirects by default, so we need to disable it
        client_no_redirect = TestClient(app, follow_redirects=False)
        response = client_no_redirect.get("/")
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"