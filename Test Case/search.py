import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=2000)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_search(page):
    #Skenario 4: Pastikan hasil pencarian menggunakan employee name menampilkan employee yang sesuai pada table
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")

    page.click("span:text('PIM')")

    employee_name = page.get_by_placeholder("Type for hints...").first
    employee_name.fill("Clair")
    page.click("button[type='submit']")

    table_row = page.locator("div.oxd-table-card").first
    expect(table_row).to_be_visible()
    expect(table_row).to_contain_text("Clair")