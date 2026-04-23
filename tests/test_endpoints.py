from unittest.mock import MagicMock, patch
from app.router.url_router import create_url,redirect_url,get_user_url,delete_url
from tests.test_conftest import auth_headers,client,test_db
from fastapi import Depends, HTTPException
import app.router.url_router as router_mod
from datetime import datetime, timezone, timedelta


#User creates url
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

#Create url with no login/access token
def test_create_url_Unauthorized(client):
    with patch("app.services.token_service.is_blacklisted", return_value=False):
        response = client.post(
            "/urls/",
            json={"original_url" : "https://google.com"}
        )
        print(response.json())
        assert response.status_code == 401
        
#User creates Invalid url, not following Anyhttpurl
def test_create_url_invalid(auth_headers,client):
    with patch("app.services.token_service.is_blacklisted",return_value=False):
        response = client.post(
            "/urls/",
            json={"original_url":"/google.com"},
            headers=auth_headers
        )
        assert response.status_code == 422

#Redirect not found, wrong url, right url but original url deacitvated
@patch("app.services.cache_service.rate_limit_redirect")
@patch("app.services.url_service.get_url_by_code")
def test_redirect_url_not_found(mock_redis,mock_get_url_by_code,client):
        mock_redis.return_value = None
        mock_get_url_by_code.side_effect = HTTPException(status_code=404)

        response = client.get("/sidhf")
        assert response.status_code == 404

#User creates a url with blocked url or private ip
def test_create_url_prv_ip(client,auth_headers):
     with patch("app.services.token_service.is_blacklisted",return_value=False):
           response = client.post(
            "/urls/",
            json={"original_url":"http://localhost:8000/auth/google/login"},
            headers=auth_headers
            )
           print(response.json())
           print(response.status_code)
           assert response.status_code == 400


# Redirect url success
@patch("app.services.cache_service.rate_limit_redirect", return_value=None)
@patch("app.services.url_service.get_url_by_code", return_value="http://google.com")
def test_redirect_url_success(mock_get_url_by_code,mock_rate,client):
        print(mock_get_url_by_code.called)
        response = client.get("/urls/cOAB9P ",follow_redirects=False)
        assert response.status_code == 302


#Get user url's, from access token in auth
def test_get_user_url(auth_headers,client):
      with patch("app.services.url_service.get_user_by_url",return_value=[
    {
        "short_code": "abc123",
        "original_url": "https://google.com",
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7)
    }
]):
            response = client.get("/urls",headers=auth_headers)
            assert response.status_code == 200
            

#Authorized user deleting url
def test_delete_url_owner(client,auth_headers):
      with patch("app.services.url_service.deactivate_url",return_value=True):
            response = client.delete(
                  "/urls/abcs",
                  headers=auth_headers
            )
            assert response.json()["message"]=="Url deactivated"
            assert response.status_code == 200

#Unauthorized user deleting url
def test_delete_url_non_owner(client):
    response = client.delete("/urls/ahsfd")
    assert response.status_code == 401

#User call his url stats
def test_get_url_stats(client,auth_headers):
     with patch("app.services.url_service.get_url_stats",return_value=
    {   "click_count":3,
        "short_code": "abc123",
        "original_url": "https://google.com",
        "created_at": datetime.now(timezone.utc),
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7)}):
          response = client.get("/urls/home/stats",
                                headers=auth_headers)
          
          assert response.status_code == 200

#User redirect but url is not active
@patch("app.services.cache_service.rate_limit_redirect",return_value=False)
@patch("app.services.url_service.get_url_by_code")      
def test_redirect_inactive(patch_func,patch_rate,client,auth_headers):
     patch_func.side_effect = HTTPException(
          status_code = 410, detail = "Url gone"
     )
     response = client.get("/urls/cOAB9P",
                           follow_redirects = False)
     
     assert response.status_code == 410

#User redirect but link expired
@patch("app.services.cache_service.rate_limit_redirect",return_value=False)
@patch("app.services.url_service.get_url_by_code")
def test_redirect_expired(p_code,p_rate,client):
     p_code.side_effect = HTTPException(
          status_code=410,detail="Url gone"
     )
     response = client.get("/urls/asdf")

     assert response.status_code == 410

     
    
          
          



