# test_github_api.py
# """
# Those are libraries for pytest (check app.py for their usage)
# """
import pytest
import unittest
from unittest.mock import patch, MagicMock
from github_api import (
    get_github_user_year_contributions,
    get_user_contributed_repos,
    calculate_rating,
    get_feedback,
)

# Mocked data for testing
username = "testuser"
github_token = "testtoken"

@pytest.fixture(name="client")
def create_connection(test_app):
    """Fixture to create a test client for the Flask app."""
    return test_app.test_client()

@pytest.fixture(name="database")
def creat_db(test_app):
    """Fixture to set up and tear down a mock database for testing."""
    with test_app.app_context():
        db = test_app.config["MONGO_CONN"].note_app
        db.blogs.insert_one({"title": "Test Blog Title", "main_body": "Test body", "owner":"test user"})
        yield db
        db.blogs.delete_one({"title": "Note Title", "owner":"test user"})

def test_get_user_contributed_repos():
    # Test the function with valid inputs
    repos_info = get_user_contributed_repos(username, github_token)
    assert isinstance(repos_info, dict)

def test_calculate_rating():
    # Test the function with valid inputs
    rating_data = {
        "Contributed Repos": {},
        "Public Repos": 5,
        "Year Contributions": {
            "totalCommitContributions": 100,
            "totalIssueContributions": 50,
            "totalPullRequestContributions": 30,
            "totalPullRequestReviewContributions": 20,
        },
        "Recent Repositories": [
            {"Forks": 10, "Languages": {"Python": 100, "JavaScript": 50}},
            {"Forks": 5, "Languages": {"Java": 80, "JavaScript": 30}},
        ],
    }
    rating = calculate_rating(rating_data)
    assert 0 <= rating <= 100

def test_get_feedback():
    # Test the function with valid inputs
    feedback = get_feedback(username, 90)
    assert isinstance(feedback, str)

class TestGitHubAPI(unittest.TestCase):
    @patch('requests.post')
    def test_get_github_user_year_contributions(self, mock_post):
        # Mocking the response from GitHub API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': {'user': {'contributionsCollection': {'totalCommitContributions': 10}}}}
        mock_post.return_value = mock_response

        # Testing the function
        result = get_github_user_year_contributions('testuser', 'testtoken')

        # Assertions
        self.assertEqual(result['totalCommitContributions'], 10)

    @patch('requests.get')
    def test_get_user_contributed_repos(self, mock_get):
        # Mocking the response from GitHub API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [{'repository': {'full_name': 'test/repo'}}]}
        mock_get.return_value = mock_response

        # Testing the function
        result = get_user_contributed_repos('testuser', 'testtoken')

        # Assertions
        self.assertIn('test/repo', result)

    def test_get_feedback(self):
        # Testing the function
        result = get_feedback('testuser', 90)

        # Assertions
        self.assertIsInstance(result, str)

# Please add more tests based on different scenarios and edge cases.
        
# Run the coverage test using the following codes: pytest --cov=github_api --cov-report term-missing test_github_api.py