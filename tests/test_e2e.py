import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

def test_home_exists(page: Page):
    
    page.goto("http://127.0.0.1:8000/")

    # expect title to contain "BILL"
    # expect(page).to_have_title(re.compile("ois"))

    expect(page.locator("h1")).to_have_text(re.compile("ois"))

    # Click the get started link.
    page.get_by_role("link", name="Get started").click()

    # Expects page to have a heading with the name of Installation.
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()

