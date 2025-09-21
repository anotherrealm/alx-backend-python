#!/usr/bin/env python3
"""
Unit & integration tests for client.py
Covers GithubOrgClient methods and end-to-end behaviour.
"""
import unittest
from typing import Any, Dict
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class

import client
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        """org property must call get_json with correct URL."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        gh = client.GithubOrgClient(org_name)
        self.assertEqual(gh.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: PropertyMock) -> None:
        """_public_repos_url should match repos_url from org payload."""
        mock_org.return_value = {"repos_url": "http://example.com/repos"}
        gh = client.GithubOrgClient("google")
        self.assertEqual(gh._public_repos_url, "http://example.com/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_url: PropertyMock, mock_get_json: Mock) -> None:
        """public_repos should return the names of all repos."""
        mock_url.return_value = "http://example.com/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        gh = client.GithubOrgClient("google")
        self.assertEqual(gh.public_repos(), ["repo1", "repo2"])
        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any], license_key: str, expected: bool) -> None:
        """has_license should match license keys properly."""
        self.assertEqual(
            client.GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient.public_repos
    Uses fixtures and mocks only network calls.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Start patcher for requests.get to return fixture data."""
        def fake_get(url: str) -> Mock:
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock = Mock()
                mock.json.return_value = cls.org_payload
                return mock
            if url == cls.org_payload["repos_url"]:
                mock = Mock()
                mock.json.return_value = cls.repos_payload
                return mock
            raise ValueError(f"Unexpected URL {url}")

        cls.get_patcher = patch("requests.get", side_effect=fake_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """public_repos returns expected repos list from fixture."""
        gh = client.GithubOrgClient(self.org_payload["login"])
        self.assertEqual(gh.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Filtering by license works correctly."""
        gh = client.GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            gh.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()