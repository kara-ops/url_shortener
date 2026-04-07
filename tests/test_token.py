from unittest.mock import patch, MagicMock
from app.services.token_service import store_refresh_token

def test_store_refresh_token():
    mock_redis = MagicMock()

    with patch("app.services.token_service.get_redis", return_value = mock_redis):
        store_refresh_token(1,"My_Token")

        mock_redis.setex.assert_called_once_with(
            "refresh:1",
            60*60*24*7,
            "My_Token"
        )