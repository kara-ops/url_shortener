from unittest.mock import MagicMock, patch
from app.router.url_router import create_url,redirect_url,get_user_url,delete_url
from tests.test_conftest import auth_headers,client,test_db
from fastapi import Depends, HTTPException
import app.router.url_router as router_mod
from datetime import datetime, timezone, timedelta



# mock_blacklist = False
# @patch("app.services.token_service.is_blacklisted", return_value=mock_blacklist)
# def test_create_url_success(mock_blacklist,client,auth_headers):
#     response = client.post(
#         "/urls/",
#         json={"original_url" : "https://google.com"},
#         headers=auth_headers
#     )
#     assert response.status_code == 200
#     assert "short_code" in response.json()

# def tests_create_url_Unauthorized(client):
#     with patch("app.services.token_service.is_blacklisted", return_value=False):
#         response = client.post(
#             "/urls/",
#             json={"original_url" : "https://google.com"}
#         )
#         print(response.json())
#         assert response.status_code == 422
        

# def test_create_url_invalid(auth_headers,client):
#     with patch("app.services.token_service.is_blacklisted",return_value=False):
#         response = client.post(
#             "/urls/",
#             json={"original_url":"/google.com"},
#             headers=auth_headers
#         )
#         assert response.status_code == 422


# @patch("app.services.cache_service.rate_limit_redirect")
# @patch("app.services.url_service.get_url_by_code")
# def test_redirect_url_not_found(mock_redis,mock_get_url_by_code,client):
#         mock_redis.return_value = None
#         mock_get_url_by_code.side_effect = HTTPException(status_code=404)

#         response = client.get("/sidhf")
#         assert response.status_code == 404

# def test_create_url_prv_ip(client,auth_headers):
#      with patch("app.services.token_service.is_blacklisted",return_value=False):
#            response = client.post(
#             "/urls/",
#             json={"original_url":"http://localhost:8000/auth/google/login"},
#             headers=auth_headers
#             )
#            print(response.json())
#            print(response.status_code)
#            assert response.status_code == 400


# @patch.object(router_mod.cache_service, "rate_limit_redirect", return_value=None)
# @patch.object(router_mod.url_service, "get_url_by_code", return_value="https://google.com")
# def test_redirect_url_success(mock_get_url_by_code,mock_rate,client):
#         print(mock_get_url_by_code.called)

#         mock_rate.return_value = None
#         mock_get_url_by_code.return_value = "https://google.com"
        
#         response = client.get("/adfd",follow_redirects=False)
#         assert response.status_code == 302


# def test_get_user_url(auth_headers,client):
#       with patch("app.services.url_service.get_user_by_url",return_value=[
#     {
#         "short_code": "abc123",
#         "original_url": "https://google.com",
#         "created_at": datetime.now(timezone.utc),
#         "expires_at": datetime.now(timezone.utc) + timedelta(days=7)
#     }
# ]):
#             response = client.get("/urls",headers=auth_headers)
#             assert response.status_code == 200
            


def test_delete_url_owner(client,auth_headers):
      with patch("app.services.url_service.deactivate_url",return_value=True):
            response = client.delete(
                  "/urls/abcs",
                  headers=auth_headers
            )
            assert response.json()["message"]=="Url deactivated"
            assert response.status_code == 20