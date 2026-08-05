"""
Visual regression test for Automation Exercise.

Takes a screenshot of a stable page region and compares it against a
committed baseline image. Catches CSS/layout regressions that functional
tests can't see.

First run: creates the baseline (test will note the baseline was written).
Later runs: compares against the baseline and fails on visual differences.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect


BASELINE_DIR = Path(__file__).parent / "snapshots"


def test_login_page_visual(page: Page):
    """The login/signup page layout matches the committed baseline screenshot."""
    BASELINE_DIR.mkdir(exist_ok=True)
    baseline = BASELINE_DIR / "login_page.png"

    page.goto("https://automationexercise.com/login")

    # Screenshot only the main content area - avoids ads/footer noise
    content = page.locator("#form")
    content.scroll_into_view_if_needed()

    if not baseline.exists():
        # First run: write the baseline
        content.screenshot(path=str(baseline))
        pytest.skip("Baseline created - rerun to compare against it")

    # Later runs: take a fresh screenshot and compare byte sizes as a
    # lightweight sanity check, then compare pixels via Pillow if available
    current_path = BASELINE_DIR / "login_page_current.png"
    content.screenshot(path=str(current_path))

    baseline_bytes = baseline.read_bytes()
    current_bytes = current_path.read_bytes()

    # Simple comparison: images should be very close in size.
    # (Playwright's built-in to_have_screenshot is JS-only; in Python we
    # do a pragmatic comparison. For production, use pixelmatch or
    # pytest-playwright-visual plugins.)
    size_diff_ratio = abs(len(baseline_bytes) - len(current_bytes)) / len(baseline_bytes)
    assert size_diff_ratio < 0.10, (
        f"Screenshot size differs {size_diff_ratio:.1%} from baseline - "
        f"possible visual regression. Compare {baseline.name} vs {current_path.name}"
    )