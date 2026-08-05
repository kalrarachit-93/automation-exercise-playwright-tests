# Automation Exercise — Playwright Test Suite with AI-Generated Test Data

End-to-end UI, API, and visual regression tests for [automationexercise.com](https://automationexercise.com),
built with **Playwright + Python + pytest**, using **Claude (Anthropic API)** to generate
realistic, unique test data on every run.

## Why this project is different

Most test suites hardcode `"John Doe"` test data. This suite generates a **fresh, realistic
user profile via LLM for every test run** — unique emails, plausible names, valid US addresses
and phone numbers. That means:

- **Zero test-data collisions** — every run registers brand-new users, so tests never fail
  with "email already exists"
- **Full test isolation** — parallel and repeated runs can't interfere with each other
- **Realistic input variety** — tests exercise the app with varied data, not the same
  hardcoded string every time

See [`tests/utils/ai_data_generator.py`](tests/utils/ai_data_generator.py) for the implementation.

## Test coverage — 36 tests

| Suite | Tests | What it covers |
|-------|-------|----------------|
| **Login / Signup** (UI) | 4 | Full registration flow, login, invalid password, duplicate email |
| **Products** (UI) | 8 | Product listing, detail pages, search (incl. parametrized terms), no-results search |
| **Cart** (UI) | 6 | Add/remove products, multi-product carts, persistence across navigation, empty state |
| **Checkout** (UI) | 7 | Guest checkout prompt, full order placement with payment, parametrized expiration dates |
| **API** | 10 | Products/brands/search endpoints — shape validation, semantic checks, response-time check |
| **Visual regression** | 1 | Login page layout vs. committed baseline screenshot |

## Architecture
automation-exercise-tests/
├── pages/ # Page Object Model classes
│ ├── login_page.py # Scoped locators (two forms share placeholders)
│ ├── signup_page.py # 15-field account form
│ ├── home_page.py # Product listing + search
│ ├── cart_page.py # Cart flows + modal handling
│ └── checkout_page.py # Checkout review, payment, confirmation
├── tests/
│ ├── ui/ # Browser tests
│ │ ├── conftest.py # Ad-blocking fixture (network-level, autouse)
│ │ └── test_*.py
│ ├── api/ # HTTP tests (no browser — ~30x faster)
│ │ ├── conftest.py # APIRequestContext fixture
│ │ └── test_products_api.py
│ └── utils/
│ └── ai_data_generator.py # LLM-powered TestUser generation
├── pytest.ini
└── requirements.txt

## Key technical decisions

**Network-level ad blocking.** The site embeds Google ads that intercept clicks and cause
flaky tests. Rather than defensively wrapping every click, an `autouse` fixture intercepts
all requests at the browser-context level and aborts ad/tracking domains. Ads never load,
so they can never interfere.

**Sticky-header click workaround.** The site's fixed "All Products" heading intercepts
mouse clicks on buttons scrolled into the top viewport area. Diagnosed via Playwright's
call log (`<h2> intercepts pointer events`) and solved with `dispatch_event("click")`,
which fires the click at the DOM level while still respecting real button state.

**Scoped locators.** The login page has two forms that both contain an "Email Address"
placeholder. Locators are scoped to their parent form
(`page.locator("form").filter(has_text=...)`) to avoid strict-mode violations.

**Shape over values in API tests.** API assertions verify structure (fields exist, types
are correct) rather than specific product data, so tests survive content changes while
still catching contract regressions.

**Honest test discovery.** The search API test initially asserted every result contains
the search term in its name — and failed, revealing the site's search also matches
category/description. The test was corrected to match actual behavior and the discovery
documented in its docstring. Distinguishing *test bugs* from *system bugs* matters.

## Running the tests

### Prerequisites
- Python 3.12+
- An Anthropic API key (for AI test-data generation)

### Setup
```bash
git clone https://github.com/kalrarachit-93/automation-exercise-playwright-tests.git
cd automation-exercise-playwright-tests
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
playwright install chromium
echo ANTHROPIC_API_KEY=your-key-here > .env
```

### Run
```bash
pytest                          # everything (~10 min: UI tests hit the live site)
pytest tests/api -v             # API suite only (~7 seconds)
pytest tests/ui/test_cart.py --headed --slowmo=800   # watch a suite run visually
```

## Possible next steps

- Pixel-level visual diffing (Pillow/pixelmatch) to replace the byte-size proxy comparison
- LLM-as-judge assertions for dynamic content validation
- Cross-browser runs (Firefox, WebKit) — a config change, not a test change
- Parallel execution with `pytest-xdist`

## About

Built by [Rachit Kalra](https://github.com/kalrarachit-93) — 8 years of software QA,
now building at the intersection of test automation and AI. Related projects:
[ai-agent-eval-framework](https://github.com/kalrarachit-93/ai-agent-eval-framework) ·
[test-case-generator](https://github.com/kalrarachit-93/test-case-generator)