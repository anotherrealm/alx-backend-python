#!/usr/bin/env python3
"""
Unit tests for utils.py
Covers access_nested_map, get_json and memoize decorator.
"""
import unittest
from typing import Any, Dict, Tuple
from parameterized import parameterized # type: ignore
from unittest.mock import patch, Mock

import utils


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: Dict[str, Any],
        path: Tuple[str, ...], expected: Any
    ) -> None:
        self.assertEqual(
            utils.access_nested_map(nested_map, path),
            expected
        )

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str, ...]
    ) -> None:
        with self.assertRaises(KeyError) as cm:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """Unit tests for utils.get_json."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(
        self, test_url: str, test_payload: Dict[str, Any], mock_get: Mock
    ) -> None:
        mock_get.return_value.json.return_value = test_payload
        self.assertEqual(utils.get_json(test_url), test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Unit tests for utils.memoize."""

    def test_memoize(self) -> None:
        class TestClass:
            def a_method(self) -> int:
                return 42

            @utils.memoize
            def a_property(self) -> int:
                return self.a_method()

        obj = TestClass()
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
