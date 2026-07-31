import pytest
from app.url_validator import validate_url

def test_valid_url():
    url = "http://www.google.com"
    result_url = "https://www.google.com"
    assert result_url == validate_url(url)

def test_blocked_domain_url():
    url = "https://evil.com/login"
    with pytest.raises(ValueError) as exc_info:
        validate_url(url)
    assert "This URL is Blocked" in str(exc_info.value)

def test_too_long_url():
    url = "https://example.com" + "a"*2050
    with pytest.raises(ValueError) as exc_info:
        validate_url(url)
    assert "URL exceed max url length" in str(exc_info.value)

def test_normalize_url():
    url = "https://GOOGLE.COM"
    result_url = "https://google.com"
    assert result_url == validate_url(url)