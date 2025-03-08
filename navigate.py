from selenium.webdriver.common.by import By

def navigate_to_page(driver):
    button_containers = []

    # Locate the button container
    while not button_containers:
        button_containers = driver.find_elements(By.TAG_NAME, "h-home-header")

    if button_containers:
        # Assuming the first "h-home-header" contains the buttons
        button_container = button_containers[0]

        # Find the pizza button inside the container
        button = button_container.find_elements(By.CLASS_NAME, "link")

        if button:
            button[0].click()  # Click the first pizza button
            print("Button clicked!")
        else:
            print("No Button found.")
    else:
        print("No button container found.")