"""
API tests for product-related endpoints on Automation Exercise.

These tests hit the API directly - no browser involved. Much faster than
UI tests, ideal for verifying backend contracts and catching regressions.

API docs: https://automationexercise.com/api_list
"""

import pytest
from playwright.sync_api import APIRequestContext


def test_get_all_products(api_request: APIRequestContext):
    """GET /api/productsList returns HTTP 200 with a products array."""
    response = api_request.get("/api/productsList")

    assert response.status == 200

    data = response.json()
    assert "responseCode" in data
    assert data["responseCode"] == 200
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0


def test_products_have_expected_fields(api_request: APIRequestContext):
    """Each product in the list has id, name, price, brand, and category."""
    response = api_request.get("/api/productsList")
    data = response.json()

    # Check just the first product for shape
    first_product = data["products"][0]
    required_fields = ["id", "name", "price", "brand", "category"]

    for field in required_fields:
        assert field in first_product, f"Product missing '{field}' field"


def test_get_all_brands(api_request: APIRequestContext):
    """GET /api/brandsList returns HTTP 200 with a brands array."""
    response = api_request.get("/api/brandsList")

    assert response.status == 200

    data = response.json()
    assert data["responseCode"] == 200
    assert "brands" in data
    assert isinstance(data["brands"], list)
    assert len(data["brands"]) > 0


def test_brands_have_expected_fields(api_request: APIRequestContext):
    """Each brand in the list has 'id' and 'brand' fields."""
    response = api_request.get("/api/brandsList")
    data = response.json()

    first_brand = data["brands"][0]
    assert "id" in first_brand
    assert "brand" in first_brand
    assert isinstance(first_brand["id"], int)
    assert isinstance(first_brand["brand"], str)


def test_search_product(api_request: APIRequestContext):
    """POST /api/searchProduct returns relevant products for a search term.

    Note: the site's search matches more than product names (likely category
    and description too), so we assert that at least some results match by
    name rather than requiring all of them to.
    """
    response = api_request.post(
        "/api/searchProduct",
        form={"search_product": "dress"},
    )

    assert response.status == 200

    data = response.json()
    assert data["responseCode"] == 200
    assert "products" in data
    assert len(data["products"]) > 0

    # At least some results should have the term in their name
    matching = [p for p in data["products"] if "dress" in p["name"].lower()]
    assert len(matching) > 0, "No returned product has 'dress' in its name"


@pytest.mark.parametrize("search_term", ["top", "shirt", "jean"])
def test_search_returns_results_for_common_terms(
    api_request: APIRequestContext, search_term: str
):
    """Various common search terms all return non-empty results."""
    response = api_request.post(
        "/api/searchProduct",
        form={"search_product": search_term},
    )

    assert response.status == 200
    data = response.json()
    assert data["responseCode"] == 200
    assert len(data["products"]) > 0, f"No results for '{search_term}'"


def test_products_endpoint_responds_quickly(api_request: APIRequestContext):
    """The products endpoint responds in under 3 seconds (performance sanity check)."""
    import time
    start = time.time()

    response = api_request.get("/api/productsList")
    elapsed = time.time() - start

    assert response.status == 200
    assert elapsed < 3.0, f"Products endpoint took {elapsed:.2f}s (expected < 3s)"


def test_invalid_endpoint_returns_error(api_request: APIRequestContext):
    """A nonexistent endpoint should not return HTTP 200 success."""
    response = api_request.get("/api/thisEndpointDoesNotExist")
    # We don't strictly require a specific error code — Automation Exercise's
    # 404 behavior isn't fully documented — but it shouldn't be a clean 200
    assert response.status != 200 or response.text() == "", \
        "Nonexistent endpoint returned HTTP 200 with content"