import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope='session')
def playwright():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope='session')
def browser(playwright):
    browser = playwright.chromium.launch(headless=True)  # Launch browser headlessly
    yield browser
    browser.close()

@pytest.fixture
def context(browser):
    # Create a browser context that ignores HTTPS errors
    context = browser.new_context(ignore_https_errors=True)
    yield context
    context.close()

@pytest.fixture
def page(context):
    # Create a new page within the context
    page = context.new_page()
    yield page
    page.close()

# Data for testing multiple routes
@pytest.mark.parametrize("route,expected_title", [
    ("/index", "QEU"),        # Homepage
    ("/team", "QEU"),         # Team page
    ("/contactus", "QEU"),    # Contact Us page
    ("/blog", "QEU")          # Blog page
])
def test_route(page, route, expected_title):
    url = f"https://127.0.0.1:5000{route}"
    page.goto(url, wait_until='domcontentloaded')
    assert page.title() == expected_title
    