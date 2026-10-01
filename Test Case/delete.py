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

def test_delete(page):
    #Skenario 5: Pastikan jika action delete employee menggunakan button delete pada table listing dilakukan maka data employee tidak akan muncul lagi pada table.
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    
    page.click("span:text('PIM')")
    page.click("button[type='submit']")
    first_row = page.locator("div.oxd-table-card").first
    expect(first_row).to_be_visible()
    delete_button = first_row.locator("button i.bi-trash").first
    delete_button.click()
    
    confirm_delete_button = page.locator("button.oxd-button--label-danger:text('Yes, Delete')")
    expect(confirm_delete_button).to_be_visible()
    confirm_delete_button.click()
    
    success_toast = page.locator("div.oxd-toast--success")
    expect(success_toast).to_be_visible()