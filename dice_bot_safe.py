from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Setup ChromeDriver
chrome_service = Service("PATH_TO_YOUR_CHROMEDRIVER")
driver = webdriver.Chrome(service=chrome_service)

# Maximize the browser window to full screen
driver.maximize_window()

# Dice credentials
email = "YOUR_EMAIL"
password = "YOUR_PASSWORD"

# Job search parameters
job_title = "data"

def process_jobs_for_location(location):
    try:
        print(f"Starting job search for location: {location}")

        # Navigate to job search
        driver.get("https://www.dice.com/jobs")
        time.sleep(5)

        # Enter job title
        job_title_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "typeaheadInput"))
        )
        job_title_input.clear()
        job_title_input.send_keys(job_title)
        job_title_input.send_keys("\n")

        # Enter location
        location_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "google-location-search"))
        )
        location_input.clear()
        location_input.send_keys(location)
        location_input.send_keys("\n")

        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "search-card"))
        )
        print(f"Job search completed for {location}! Listings are visible.")

        # Click "Today" filter
        today_filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='posted-date-option' and contains(text(),'Today')]"))
        )
        today_filter_button.click()
        print("Filtered jobs to 'Today'.")
        time.sleep(3)  # Add a 3-second pause for the page to load

        # Loop through all pages of job listings
        while True:
            job_listings = driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")
            index = 0
            while index < len(job_listings):
                try:
                    print(f"Processing job listing {index + 1} for {location}...")

                    # Refresh job listings if stale
                    job_listings = driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")
                    job_link = job_listings[index]

                    # Scroll to the job listing to ensure it's visible
                    driver.execute_script("arguments[0].scrollIntoView(true);", job_link)
                    time.sleep(1)

                    # Use JavaScript to click to avoid interception
                    driver.execute_script("arguments[0].click();", job_link)

                    # Switch to the new tab
                    driver.switch_to.window(driver.window_handles[-1])

                    # Wait for the job details page
                    time.sleep(5)

                    # Handle external websites
                    if "dice.com" not in driver.current_url:
                        print("External website detected. Closing tab.")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        index += 1
                        continue

                    # Check for Easy Apply button
                    print("Checking for 'Easy Apply' button inside shadow DOM...")
                    try:
                        apply_button_parent = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "apply-button-wc"))
                        )
                        shadow_root = driver.execute_script("return arguments[0].shadowRoot", apply_button_parent)
                        if not shadow_root:
                            raise Exception("Shadow root not found.")

                        apply_button = shadow_root.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
                        button_text = apply_button.text.strip()
                        print(f"Button text: {button_text}")

                        if button_text.lower() == "easy apply":
                            driver.execute_script("arguments[0].click();", apply_button)
                            print("Easy Apply button clicked!")

                            # Handle form submission
                            try:
                                print("Waiting for 'Next' button...")
                                next_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                                )
                                next_button.click()
                                print("Clicked 'Next' button.")

                                print("Waiting for 'Submit' button...")
                                submit_button = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
                                )
                                submit_button.click()
                                print("Clicked 'Submit' button.")
                            except Exception as e:
                                print(f"Error during form submission: {e}")
                        else:
                            print("Button text does not match 'Easy apply'. Skipping this job.")

                    except Exception as e:
                        print(f"No Easy Apply button found or error: {e}")

                    # Close current tab and return to the search tab
                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    index += 1

                except Exception as e:
                    print(f"Error processing job listing {index + 1}: {e}")
                    driver.switch_to.window(driver.window_handles[0])
                    index += 1

            # Check if there's a "Next" page
            try:
                print("Checking for 'Next' button...")
                next_page_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'pagination-next')]"))
                )
                next_page_classes = next_page_element.get_attribute("class")

                # If the "Next" button is disabled, stop pagination
                if "disabled" in next_page_classes:
                    print("No more pages left for this location. Moving to the next location.")
                    break

                next_page_button = next_page_element.find_element(By.TAG_NAME, "a")
                driver.execute_script("arguments[0].click();", next_page_button)
                print("Moving to the next page of job listings...")
                time.sleep(5)
            except Exception as e:
                print(f"Error handling pagination or 'Next' button: {e}")
                break

    except Exception as e:
        print(f"Error occurred for location {location}: {e}")

# Login and initialize
try:
    driver.get("https://www.dice.com/dashboard/login")
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "email"))
    )
    email_input.send_keys(email)
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    continue_button.click()
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(password)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))
    print("Logged in successfully!")

    # Process jobs for all locations
    locations = ["Seattle", "Denver", "Chicago", "Washington, DC"]
    for location in locations:
        process_jobs_for_location(location)

except Exception as e:
    print(f"An error occurred: {e}")

# Pause to keep the browser open
input("Press Enter to close the browser...")
