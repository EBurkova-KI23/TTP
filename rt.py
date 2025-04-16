import pytest

def test_input_text(expected_result, actual_result):
    assert expected_result == actual_result, f"expected {expected_result}, got {actual_result}"

def test_substring(full_string, substring):
    assert substring in full_string, f"expected '{substring}' to be substring of '{full_string}'"

# Пример запусков для тестов с использованием pytest
def test_example():
    test_input_text(8, 11)
    test_input_text(11, 11)
    test_input_text(11, 15)

def test_substring_example():
    test_substring("fulltext", "some_value")
    test_substring("some_text", "some")