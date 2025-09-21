#!/usr/bin/env python3
"""
Utility functions for nested map access, JSON fetching, and memoization.
"""
import requests
from typing import Any, Dict, Tuple, Callable


def access_nested_map(nested_map: Dict[str, Any], path: Tuple[str, ...]) -> Any:
    """Access a value in a nested map using a tuple path."""
    current = nested_map
    for key in path:
        current = current[key]
    return current


def get_json(url: str) -> Dict:
    """Fetch JSON data from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(method: Callable) -> Callable:
    """Decorator to memoize method results."""
    attr_name = f"_{method.__name__}_memoized"

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return property(wrapper)