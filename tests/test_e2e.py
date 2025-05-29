import re
import pytest
from playwright.sync_api import Page, expect


# @pytest.fixture(scope="function", autouse=True)
# def before_each_after_each(page: Page):

#     # print("before the test runs")

#     # Go to the starting url before each test.
#     page.goto("http://127.0.0.1:8000/")
#     yield

#     # print("after the test runs")

TIMEOUT = 10000
expect.set_options(timeout=TIMEOUT)


def test_playwright_working(page: Page):
    page.goto("https://playwright.dev/")

    expect(page, "Playwright is not working").to_have_title(re.compile("Playwright"))


def test_home_exists(page: Page):
    page.goto("http://127.0.0.1:8000/")

    # expect heading with billinois to exist
    expect(page.locator("h1"), "Custom home page is not properly configured").to_have_text(
        "BILLinois"
    )


@pytest.mark.parametrize(
    "search_term, expected_results, message",
    [
        ("", 'Search results for ""', "Failed to prompt user when no search term entered."),
        ("asdf", "No results found.", "Failed to inform user when 0 results are returned."),
        ("environment", "Search results", "Failed to return any results for a valid search term."),
    ],
)
def test_search(page: Page, search_term, expected_results, message):
    """
    Test the search functionality of the page for at least two cases:
    - Empty search case, where all bills will be returned
    - Empty results case, where the user is notified that no results were found.
    - Non-empty results case, where the user should see results.
    """

    page.goto("http://127.0.0.1:8000/")

    # search for a bill
    page.get_by_placeholder("Search bills by name or topic...").click()
    page.keyboard.type(search_term)

    # TODO: ask frontend to add a submit button
    # page.locator('input[type="submit"][value="Search"]').click()
    page.keyboard.press("Enter")

    # expect page to have search results
    expect(page.get_by_text(expected_results), message).to_be_visible()


def test_bill_page(page: Page):
    """
    Test navigating to a specific bill page.
    TODO: finish
    """

    page.goto("http://127.0.0.1:8000/search/?query=environment")

    page.get_by_role("link", name="DCFS-YOUTH INDEPENDENCE GOAL").click()


# def test_favorite_bill(page: Page):
#     """
#     Test favoriting a bill.
#     TODO: finish
#     TODO: if not signed in, prompt to sign in
#     """

#     page.goto("http://127.0.0.1:8000/search/?query=environment")

#     page.get_by_role("link",name="Favorite").click()

#     # expect star to be filled
#     expect(page.get_by_role("link",name="Favorite")).to_have_class(re.compile("fa-star-fill"))


@pytest.mark.parametrize(
    "username, password, expected_results, message",
    [
        (
            "wrong@wrong.com",
            "testpassword",
            "not correct",
            "Failed to inform user when credentials are incorrect.",
        ),
        (
            "notkarenyi@gmail.com",
            "test123!",
            "Sign Out",
            "Failed to redirect to home page with logged-in state after successful login.",
        ),
    ],
)
def test_sign_in(page: Page, username, password, expected_results, message):
    """
    Test signing in from the home page for at least two cases:
    - Wrong username/password case, where the user is warned about incorrect credentials.
    - Successful login case, where user is redirected to home page with a logged-in state.
    """

    page.goto("http://127.0.0.1:8000/")

    # page.locator("#djHideToolBarButton").click(timeout=TIMEOUT)

    page.get_by_text("Menu").click(timeout=TIMEOUT)
    page.get_by_text("Log In").click(timeout=TIMEOUT)

    # assert page.locator('[href*="/accounts/login"]').is_visible(), "Element is not visible"
    # assert page.locator('[href*="/accounts/login"]').is_enabled(), "Element is not enabled"

    page.get_by_placeholder("Email address").click()
    page.keyboard.type(username)

    page.get_by_placeholder("Password").click()
    page.keyboard.type(password)

    page.locator("button[type='submit']").first.click()

    if expected_results == "Sign Out":  # click menu only if successful login
        page.pause()
        page.screenshot(path="debug.png")
        page.get_by_text("Menu").click(timeout=TIMEOUT)

    expect(page.get_by_text(expected_results), message).to_be_visible()
