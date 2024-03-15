from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pickle
import os

# Specify the path to your ChromeDriver executable
chrome_driver_path = "/usr/local/bin/chromedriver"

# Create a Service object
service = Service(executable_path=chrome_driver_path)

# Use the 'service' argument when creating the Chrome WebDriver instance
driver = webdriver.Chrome(service=service)

# Initially navigate to the domain to set the correct domain for the cookies
driver.get('https://oncourse.college/CS198')

# Check if the cookies file exists before trying to load it
if os.path.exists('cookies.pkl'):
    # Load previously saved cookies
    with open('cookies.pkl', 'rb') as cookies_file:
        cookies = pickle.load(cookies_file)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # Reload the page to apply the cookies, ensuring logged-in state
    driver.get('https://oncourse.college/CS198')
else:
    print("Cookies file not found. You might need to login manually and save cookies first.")

# Wait for the page to load after setting cookies
wait = WebDriverWait(driver, 60)

# Your existing code for interacting with the page goes here

# Example: Locate a trigger element and perform hover action
trigger_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas[data-zr-dom-id="zr_0"]')))
hover = ActionChains(driver).move_to_element(trigger_element)
hover.perform()

# Example: Try to locate a tooltip and print its text
tooltip = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@style, 'pointer-events: none;')]")))
tooltip_text = tooltip.text
print(tooltip_text)

# Clean up, close WebDriver
driver.quit()
