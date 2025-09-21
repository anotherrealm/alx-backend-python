#!/usr/bin/env python3
import unittest
from typing import Any, Dict
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class 
import client
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json: Mock) -> None:
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        gh = client.GithubOrgClient(org_name)
        self.assertEqual(gh.org, test_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: PropertyMock) -> None:
        mock_org.return_value = {"repos_url": "http://example.com/repos"}
        gh = client.GithubOrgClient("google")
        self.assertEqual(gh._public_repos_url, "http://example.com/repos")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_url: PropertyMock, mock_get_json: Mock) -> None:
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
    @classmethod
    def setUpClass(cls) -> None:
        def fake_get(url: str) -> Mock:
            mock = Mock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock.json.return_value = cls.repos_payload
            else:
                raise ValueError(f"Unexpected URL {url}")
            return mock
        cls.get_patcher = patch("requests.get", side_effect=fake_get)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        gh = client.GithubOrgClient(self.org_payload["login"])
        self.assertEqual(gh.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        gh = client.GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            gh.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

if __name__ == "__main__":
    unittest.main()