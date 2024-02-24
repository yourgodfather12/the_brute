## Requirements
- Python 3.x
- Selenium
- fake_useragent
- Stem
- Chrome WebDriver
- Tor Browser

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/downloads/)
2. Install required Python packages:
    ```
    pip install selenium fake_useragent stem
    ```
3. Download and install [Tor Browser](https://www.torproject.org/download/)
4. Download [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) compatible with your Chrome version and place it in your system's PATH.

## Usage

1. Start the Tor Browser and keep it running.
2. Run the script by executing the following command in your terminal:
    ```
    python login_attempt.py
    ```
3. Enter the URL of the login page when prompted. If not provided, the script will use a default URL.
4. Enter the username you want to attempt login with.
5. The script will read passwords from a file named "rockyou.txt" in the same directory. Ensure you have this file or replace the path in the script.
6. The script will launch multiple threads to attempt login with different passwords.
7. Upon completion, it will display successful and failed login attempts along with any error messages.

## Note

- Make sure to provide the correct path to the Chrome WebDriver in the script.
- Replace the default values for `username_selector`, `password_selector`, `login_button_selector`, and `success_url` with actual selectors and URLs for your login page.
- Ensure you have a valid `rockyou.txt` file containing a list of passwords.
