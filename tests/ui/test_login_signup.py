"""
Login and signup tests for Automation Exercise.

Uses AI-generated user data so each test run is independent — no
"account already exists" collisions between runs.
"""

import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from tests.utils.ai_data_generator import generate_test_user


def test_new_user_can_register(page: Page):
    """A new user can complete the full signup flow and see 'Account Created!'."""
    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    login_page.navigate()
    login_page.start_signup(user.name, user.email)

    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()


def test_registered_user_can_login(page: Page):
    """After signing up, the same user can log in with their credentials."""
    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # Register first
    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()
    signup_page.click_continue()

    # Now log out and log back in - proves the account persists
    page.get_by_role("link", name="Logout").click()
    login_page.login_as(user.email, user.password)

    # After login, "Logout" link should be visible in the nav
    expect(page.get_by_role("link", name="Logout")).to_be_visible()


def test_login_with_invalid_password_shows_error(page: Page):
    """Login with a valid email but wrong password shows the incorrect-credentials error."""
    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # Register first so the email is valid
    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()
    signup_page.click_continue()

    # Log out
    page.get_by_role("link", name="Logout").click()

    # Try login with wrong password
    login_page.login_as(user.email, "wrong-password-xyz")
    login_page.expect_login_error()


def test_signup_with_existing_email_shows_error(page: Page):
    """Attempting to signup with an already-registered email shows the 'exists' error."""
    user = generate_test_user()
    login_page = LoginPage(page)
    signup_page = SignupPage(page)

    # Register once
    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    signup_page.fill_account_details(user)
    signup_page.submit()
    signup_page.expect_account_created()
    signup_page.click_continue()

    # Log out
    page.get_by_role("link", name="Logout").click()

    # Try to signup again with the same email
    login_page.navigate()
    login_page.start_signup(user.name, user.email)
    login_page.expect_signup_error()