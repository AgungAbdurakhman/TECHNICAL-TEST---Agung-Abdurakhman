import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=3000)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_login_valid(page):
    #Skenario 1: Pastikan user dapat login dan masuk ke dashboard jika login dengan credential yang benar
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    expect(page.locator("h6.oxd-topbar-header-breadcrumb-module")).to_have_text("Dashboard")

def test_login_invalid(page):
    #Skenario 2: Pastikan message error "Invalid Credentials" muncul jika login dengan credential yang salah
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "salahpassword")
    page.click("button[type='submit']")
    error_message = page.locator("p.oxd-alert-content-text")
    expect(error_message).to_be_visible()
    expect(error_message).to_have_text("Invalid credentials")

def test_listpim(page):
    #Skenario 3: Login dengan credential yang benar -> Masuk ke menu PIM -> pastikan halaman Employee List muncul dan semua field input dalam keadaan kosong / hanya menampilkan placeholder jika punya.
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.fill("input[name='username']", "Admin")
    page.fill("input[name='password']", "admin123")
    page.click("button[type='submit']")
    page.click("span:text('PIM')")
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
    employee_name_input = page.locator("div.oxd-input-group:has-text('Employee Name') input")
    expect(employee_name_input).to_be_visible()
    assert employee_name_input.input_value() == ""

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