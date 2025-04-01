from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import traceback
import ctypes

# finds the input fields
def get_input_elements(driver):
    # Locate main view container
    try:
        main_view = driver.find_element(By.ID, "mainViewPlaceholder")
    except Exception as e:
        err_msg = f"Exception: Failed while trying to find element with ID 'mainViewPlaceholder'. \n\
            {e}\n\nTraceback:\n{traceback.format_exc()}"
        ctypes.windll.user32.MessageBoxW(0, err_msg, "Error", 0x10)
        raise Exception(err_msg)


    # Locate the input fields inside the main_view container
    input_fields = main_view.find_elements(By.TAG_NAME, "input")

    if len(input_fields) >= 2:  # Ensure there are at least two input fields
        username_input = input_fields[0]  # First input is usually username
        password_input = input_fields[1]  # Second input is usually password
    else:
        err_msg = f"Exception: username and password input fields were not found under 'mainViewPlaceholder'"
        ctypes.windll.user32.MessageBoxW(0, err_msg, "Error", 0x10)
        raise Exception(err_msg)
    return username_input, password_input

def login(conf):
    # Read credentials
    website = conf['website']
    username = conf['username']
    password  = conf['password']

    # Setup Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Open login page
    driver.get(website)  # URL from the text file

    username_input, password_input = get_input_elements(driver)

    # Enter credentials
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # Handle CAPTCHA by checking if the password field disappears
    try:
        while driver.current_url == website:
            print("CAPTCHA detected! Please solve it manually.")

            username_input, password_input = get_input_elements(driver)

            # Re-enter password
            if password_input.get_attribute("value") == "":
                password_input.send_keys(password)
                print("Password re-entered. Waiting for user to complete CAPTCHA...")

            # Wait until the user submits the CAPTCHA
            time.sleep(2)

    except Exception as e:
        print("Error while handling CAPTCHA:", e)

    print("Login successful, current page title:", driver.title)

    return driver