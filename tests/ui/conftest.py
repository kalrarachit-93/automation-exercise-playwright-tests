"""
Shared fixtures for UI tests.

Provides browser configuration and shared setup steps for all UI tests
in this folder.
"""

import pytest
from playwright.sync_api import BrowserContext


# Ad and tracking domains that Automation Exercise embeds.
# Blocking them at the network layer eliminates ad popups that would
# otherwise intercept clicks and cause flaky tests.
BLOCKED_DOMAINS = [
    "googlesyndication.com",
    "doubleclick.net",
    "googleadservices.com",
    "google-analytics.com",
    "adsystem.com",
]


@pytest.fixture(autouse=True)
def block_ads(context: BrowserContext):
    """
    Blocks ad and tracking domains for all UI tests. Applied automatically
    because of autouse=True — every test in this folder gets ads blocked
    without having to opt in.
    """
    def handler(route):
        url = route.request.url
        if any(domain in url for domain in BLOCKED_DOMAINS):
            route.abort()
        else:
            route.continue_()
    
    context.route("**/*", handler)
    yield
    # No teardown needed — the context is disposed by pytest-playwright