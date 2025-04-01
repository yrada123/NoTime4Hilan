from selenium.webdriver.common.by import By

def navigate_to_page(driver):
    button_containers = []

    # Locate the button container
    while not button_containers:
        button_containers = driver.find_elements(By.TAG_NAME, "h-home-header")

    # Assuming the first "h-home-header" contains the buttons
    button_container = button_containers[0]

    # Find the next page button inside the container
    button = button_container.find_elements(By.CLASS_NAME, "link")

    if button:
        driver.execute_script("arguments[0].click();", button[0]) # Click the first next page button
        print("Button clicked!")
    else:
        print("No Button found.")
