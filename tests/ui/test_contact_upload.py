"""
Contact form test with file upload.

Covers Playwright's set_input_files() - attaching a local file to an
<input type='file'> element without any OS file-picker dialog.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


def test_contact_form_with_file_upload(page: Page, tmp_path: Path):
    """Submit the contact form with an attached file; expect the success banner."""
    # Create a small file to upload - tmp_path is a pytest built-in fixture
    # providing a unique temp directory per test
    upload_file = tmp_path / "bug_report.txt"
    upload_file.write_text("Steps to reproduce: added item to cart, price doubled.")

    page.goto("https://automationexercise.com/contact_us")

    page.get_by_placeholder("Name").fill("Rachit Test")
    page.get_by_placeholder("Email", exact=True).fill("rachit.contact@testmail.com")
    page.get_by_placeholder("Subject").fill("Test message with attachment")
    page.get_by_placeholder("Your Message Here").fill("This is an automated test submission.")

    # The upload itself - no dialog appears; Playwright sets the file directly
    page.locator('input[name="upload_file"]').set_input_files(str(upload_file))

    # Site shows a JS confirm() dialog on submit - accept it before clicking
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Submit").click()

    expect(page.locator("#contact-page").get_by_text("Success! Your details have been submitted successfully.")).to_be_visible()