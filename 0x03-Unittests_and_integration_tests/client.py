#!/usr/bin/env python3
"""
GithubOrgClient module for interacting with GitHub API.
"""
import requests
from typing import Dict, List, Optional


def get_json(url: str) -> Dict:
    """Fetch JSON data from a URL."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Client for GitHub organization data."""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    @property
    def org(self) -> Dict:
        """Return organization info."""
        return get_json(self.ORG_URL.format(org=self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the repos_url from org info."""
        return self.org["repos_url"]

    def public_repos(self, license: Optional[str] = None) -> List[str]:
        """Return list of public repo names, optionally filtered by license."""
        repos = get_json(self._public_repos_url)
        repo_names = []
        for repo in repos:
            if license is None or self.has_license(repo, license):
                repo_names.append(repo["name"])
        return repo_names

    @staticmethod
    def has_license(repo: Dict, license_key: str) -> bool:
        """Check if repo has a specific license."""
        return repo.get("license", {}).get("key") == license_key