import pytest
from fastapi import HTTPException
from src.api.dependencies import handle_error


def test_handle_error_creates_http_exception():
    """Test that handle_error creates an HTTPException with correct status code and message."""
    error = handle_error(404, "Not Found")
    assert isinstance(error, HTTPException)
    assert error.status_code == 404
    assert error.detail == "Not Found"


def test_handle_error_with_different_codes():
    """Test that handle_error works with different status codes."""
    error_400 = handle_error(400, "Bad Request")
    assert error_400.status_code == 400
    assert error_400.detail == "Bad Request"
    
    error_500 = handle_error(500, "Internal Server Error")
    assert error_500.status_code == 500
    assert error_500.detail == "Internal Server Error"