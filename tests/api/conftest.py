"""
Shared fixtures for API tests.

API tests use Playwright's request context — no browser needed.
The api_request fixture provides a clean, reusable HTTP client.
"""

import pytest
from playwright.sync_api import Playwright, APIRequestContext


BASE_URL = "https://automationexercise.com"


@pytest.fixture
def api_request(playwright: Playwright) -> APIRequestContext:
    """
    Provides a Playwright APIRequestContext configured with the base URL.
    Use for HTTP calls to Automation Exercise's API endpoints.
    """
    request_context = playwright.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()