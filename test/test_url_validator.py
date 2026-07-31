import pytest
from app.url_validator import validate_url


@pytest.mark.parametrize("input_url, output_url", [
    ("http://www.google.com", "https://www.google.com"),
    ("http://www.GOOGLE.com", "https://www.google.com"),
    ("https://example.com/path", "https://example.com/path"),
])
def test_valid_url(input_url, output_url):
    assert output_url == validate_url(input_url)

@pytest.mark.parametrize("blocked_url", [
    "http://phishing.example.com/test",
    "https://evil.com/login",
])
def test_blocked_domain_url(blocked_url):
    with pytest.raises(ValueError) as exc_info:
        validate_url(blocked_url)
    assert "This URL is Blocked" in str(exc_info.value)

def test_too_long_url():
    url = "https://example.com" + "a"*2050
    with pytest.raises(ValueError) as exc_info:
        validate_url(url)
    assert "URL exceed max url length" in str(exc_info.value)