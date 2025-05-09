import re
import pytest
from playwright.sync_api import Page, expect

def test_playwright_working(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))


def test_home_exists(page: Page):
    page.goto("http://127.0.0.1:8000/")

    # expect heading with billinois to exist"
    expect(page.locator("h1")).to_have_text(re.compile("ois"))


@pytest.mark.parametrize(
    "search_term, expected_results",
    [
        ("", "Please enter a search term."),
        # ("e", "No results found."),
        ("environment", "Topics"),
    ],
)
def test_search_empty(page: Page, search_term, expected_results):
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
    expect(page.get_by_text(expected_results)).to_be_visible()

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
