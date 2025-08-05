import sys
import json
import os
import re # Import the regular expression module
from playwright.sync_api import sync_playwright, TimeoutError

# Define the path for storing session data. This path is inside the container.
SESSION_FILE_PATH = "/session_data/assetmark_session.json"
DEBUG_SCREENSHOT_PATH = "/session_data/debug_screenshot.png"

def perform_manual_auth(username, password):
    """
    Performs a manual, headed login to handle MFA and save the session state.
    You only need to run this once every 90 days.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            print("--- Manual Authentication Required ---")
            login_url = "https://www.ewealthmanager.com/ewmLogin/account/login"
            page.goto(login_url, timeout=60000)
            print("1. Browser opened. Please log in.")

            page.fill("#okta-signin-username", username)
            page.fill("#okta-signin-password", password)
            page.click("#okta-signin-submit")
            print("2. Credentials submitted.")

            print("3. Please complete the MFA step in the browser.")
            print("4. IMPORTANT: Check the 'Do not challenge me on this device...' box.")
            
            print("Waiting for dashboard navigation...")
            page.wait_for_url("**/investorportal/overview/**", timeout=300000)
            print("Navigation to dashboard complete.")
            
            # Use the most precise XPath selector to find the balance element.
            print("Looking for 'Total Investments' balance element...")
            balance_selector = "//div[text()='Total Investments']/following-sibling::div[contains(@class, 'currency-child__container')][1]"
            page.wait_for_selector(balance_selector, timeout=60000)
            print("5. Login successful! Dashboard detected.")

            page.context.storage_state(path=SESSION_FILE_PATH)
            print(f"6. Session state successfully saved to {SESSION_FILE_PATH}")

        except Exception as e:
            print("An error occurred. Taking a screenshot for debugging...")
            page.screenshot(path=DEBUG_SCREENSHOT_PATH, full_page=True)
            print(f"Screenshot saved to {DEBUG_SCREENSHOT_PATH} inside the container.")
            print(f"An error occurred during manual authentication: {str(e)}")
        finally:
            browser.close()

def run_automated_scraper():
    """
    Runs the scraper in headless mode using a saved session file.
    This is what n8n will execute for daily runs.
    """
    if not os.path.exists(SESSION_FILE_PATH):
        error_data = {"error": "Session file not found. Please run with the --auth flag first."}
        print(json.dumps(error_data, indent=2))
        return

    scraped_data = {"account_name": "AssetMark IRA", "balance": None, "holdings": [], "error": None}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=SESSION_FILE_PATH)
        page = context.new_page()

        try:
            dashboard_url = "https://www.ewealthmanager.com/investorportal/overview/"
            page.goto(dashboard_url, timeout=60000)

            print("Waiting for network to be idle...")
            page.wait_for_load_state('networkidle', timeout=60000)
            print("Network is idle.")

            print("Waiting for main dashboard title 'Overview'...")
            overview_title_selector = "a:has-text('Overview')"
            page.wait_for_selector(overview_title_selector, timeout=60000)
            print("Dashboard title detected. Page should be fully loaded.")

            try:
                close_button_selector = '[aria-label*="close" i], [class*="close" i]'
                page.locator(close_button_selector).first.click(timeout=5000)
                print("Potential pop-up window closed.")
            except TimeoutError:
                print("No pop-up window found, continuing...")

            # --- FINAL, ULTRA-PRECISE XPATH SELECTOR ---
            # This XPath is the most robust way to find the balance. It finds the div
            # with the exact text "Total Investments" and then selects its immediate sibling div
            # THAT ALSO CONTAINS the specific class name we identified. This is unambiguous.
            print("Looking for balance element with ultra-precise XPath...")
            balance_selector = "//div[text()='Total Investments']/following-sibling::div[contains(@class, 'currency-child__container')][1]"
            balance_element_locator = page.locator(balance_selector)
            
            balance_text = balance_element_locator.inner_text(timeout=90000)
            print("Balance element found and text retrieved.")
            # --- END OF FINAL SELECTOR ---

            cleaned_text = balance_text.replace('$', '').replace(',', '').replace('\u2009', '')
            scraped_data["balance"] = float(cleaned_text)

        except Exception as e:
            print("An error occurred during automated run. Taking a screenshot for debugging...")
            page.screenshot(path=DEBUG_SCREENSHOT_PATH, full_page=True)
            print(f"Screenshot saved to {DEBUG_SCREENSHOT_PATH} inside the container.")
            scraped_data["error"] = f"An unexpected error occurred during scraping: {str(e)}"
        finally:
            browser.close()
            print(json.dumps(scraped_data, indent=2))

if __name__ == "__main__":
    if "--auth" in sys.argv:
        if len(sys.argv) != 4:
            print("Usage: python scrape_assetmark.py --auth <username> <password>")
            sys.exit(1)
        user = sys.argv[2]
        pwd = sys.argv[3]
        perform_manual_auth(user, pwd)
    else:
        run_automated_scraper()
