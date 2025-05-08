import re
import pytest
from playwright.sync_api import Page, expect

def test_playwright_working(page: Page):
    page.goto("https://playwright.dev/")

    expect(page, "Playwright is not working").to_have_title(re.compile("Playwright"))


def test_home_exists(page: Page):
    page.goto("http://127.0.0.1:8000/")

    # expect heading with billinois to exist
    expect(page.locator("h1"), "Custom home page is not properly configured").to_have_text("BILLinois")


@pytest.mark.parametrize(
    "search_term, expected_results, message",
    [
        ("", "Please enter a search term.", "Failed to prompt user when no search term entered."),
        ("e", "No results found.", "Failed to inform user when 0 results are returned."),
        ("environment", "Topics", "Failed to return any results for a valid search term."),
    ],
)
def test_search_empty(page: Page, search_term, expected_results, message):
    """
    Test the search functionality of the page for at least two cases:
    - Empty search case, where the user is prompted to enter a search term.
    - Empty results case, where the user is notified that no results were found.
    - Non-empty results case, where the user should see results.
    """

    page.goto("http://127.0.0.1:8000/")

    # search for a bill
    page.get_by_placeholder("Search Bill Summary").click()
    page.keyboard.type(search_term)

    page.locator('input[type="submit"][value="Search"]').click()

    # expect page to have search results
    expect(page.get_by_text(expected_results), message).to_be_visible()

def test_bill_page(page: Page):
    """
    Test navigating to a specific bill page.
    TODO: finish
    """

    page.goto("http://127.0.0.1:8000/search/?query=environment")

    page.get_by_role("link",name="HR 191").click()

def test_favorite_bill(page: Page):
    """
    Test favoriting a bill. 
    TODO: finish
    TODO: if not signed in, prompt to sign in
    """

    page.goto("http://127.0.0.1:8000/search/?query=environment")

    page.get_by_role("link",name="Favorite").click()

    # expect star to be filled
    expect(page.get_by_role("link",name="Favorite")).to_have_class(re.compile("fa-star-fill"))

def test_sign_in(page: Page):
    """
    Test signing in from the home page.
    TODO: finish
    """

    page.goto("http://127.0.0.1:8000/")

    page.get_by_role("link",name="Sign in").click()

    # expect page to have search results
    expect(page.get_by_text("Sign in")).to_be_visible()
