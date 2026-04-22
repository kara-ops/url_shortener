from unittest.mock import MagicMock, patch
from app.router.url_router import create_url,redirect_url
from tests.test_conftest import auth_headers,client,test_db
from fastapi import Depends, HTTPException


mock_blacklist = False
@patch("app.services.token_service.is_blacklisted", return_value=mock_blacklist)
def test_create_url_success(mock_blacklist,client,auth_headers):
    response = client.post(
        "/urls/",
        json={"original_url" : "https://google.com"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "short_code" in response.json()

def tests_create_url_Unauthorized(client):
    with patch("app.services.token_service.is_blacklisted", return_value=False):
        response = client.post(
            "/urls/",
            json={"original_url" : "https://google.com"}
        )
        print(response.json())
        assert response.status_code == 422
        

def test_create_url_invalid(auth_headers,client):
    with patch("app.services.token_service.is_blacklisted",return_value=False):
        response = client.post(
            "/urls/",
            json={"original_url":"/google.com"},
            headers=auth_headers
        )
        assert response.status_code == 422


@patch("app.services.cache_service.rate_limit_redirect")
@patch("app.services.url_service.get_url_by_code")
def test_redirect_url_not_found(mock_redis,mock_get_url_by_code,client):
        mock_redis.return_value = None
        mock_get_url_by_code.side_effect = HTTPException(status_code=404)

        response = client.get("/sidhf")
        assert response.status_code == 404
