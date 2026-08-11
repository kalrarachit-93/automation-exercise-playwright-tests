"""
Shared fixtures for UI tests.

Provides browser configuration and shared setup steps for all UI tests
in this folder.
"""

import pytest
from playwright.sync_api import BrowserContext

import json
from pathlib import Path

from playwright.sync_api import Browser

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from tests.utils.ai_data_generator import generate_test_user


AUTH_DIR = Path(__file__).parent / ".auth"

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

@pytest.fixture(scope="session")
def registered_user(browser: Browser):
    """
    Session-scoped: registers ONE user via the UI at the start of the test
    session, saves the authenticated browser state to disk, and returns
    (user, state_path). Every test that needs a logged-in session reuses
    this state instead of re-registering through the UI.
    """
    AUTH_DIR.mkdir(exist_ok=True)
    state_path = AUTH_DIR / "user_state.json"

    context = browser.new_context()
    page = context.new_page()

    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()
    signup_page.click_continue()

    context.storage_state(path=str(state_path))
    context.close()

    return user, state_path

@pytest.fixture
def logged_in_page(browser: Browser, registered_user):
    """
    Function-scoped: a fresh page that starts ALREADY LOGGED IN, using the
    session user's saved storage state. No UI login is performed.
    """
    user, state_path = registered_user
    context = browser.new_context(storage_state=str(state_path))
    context.route("**/*", lambda route: route.abort()
    if any(d in route.request.url for d in BLOCKED_DOMAINS)
    else route.continue_())
    page = context.new_page()
    yield page
    context.close()

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