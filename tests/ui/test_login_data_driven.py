"""
Data-driven login tests for Automation Exercise.

Test data lives in test_data/login_scenarios.csv - the test function is
written once and runs once per CSV row. Adding a new scenario means
adding a CSV line, not writing code: manual QAs and BAs can extend
coverage by editing the spreadsheet.

Pattern: load the CSV at collection time, feed rows to parametrize.
"""

import csv
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "login_scenarios.csv"


def load_login_scenarios():
    """Read the CSV and return a list of (scenario, email, password, expected) tuples."""
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            (row["scenario"], row["email"], row["password"], row["expected_result"])
            for row in reader
        ]


@pytest.mark.parametrize(
    "scenario,email,password,expected_result",
    load_login_scenarios(),
    ids=[row[0] for row in load_login_scenarios()],
)
def test_login_from_csv(page: Page, scenario, email, password, expected_result):
    """Each CSV row is one login attempt with an expected outcome."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login_as(email, password)

    if expected_result == "server_error":
        login_page.expect_login_error()
    elif expected_result == "client_blocked":
        login_page.expect_client_side_block()