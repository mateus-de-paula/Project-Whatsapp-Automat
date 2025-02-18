# Project-Whatsapp-Automat
 Educational message automation via Whatsspp

## Overview
This project automates the process of sending personalized messages to clients via WhatsApp. It allows users to send customized messages to multiple contacts using data from a CSV file. The program reads the client information from the CSV file, including their names and phone numbers, and sends three messages to each contact: a greeting, the main message body, and a closing message.

## Features
- Automates the process of sending messages to multiple clients efficiently.
- Personalizes messages by replacing placeholders with client names.
- Supports sending messages through WhatsApp Web.
- Utilizes a Chrome WebDriver for browser automation.
- Provides a user-friendly interface for configuring message templates and loading client data from CSV files.

## Installation
1. Clone this repository to your local machine.
   ```
   git clone https://github.com/yourusername/whatsapp-message-automation.git
   ```
2. Install the required dependencies using pip.
   ```
   pip install -r requirements.txt
   ```
3. Download and install the Chrome WebDriver.
   - [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/)

## Chrome Profile Path Configuration

For the program to work optimally, it is adviced to create a Chrome profile so that your eShop Prices login is maintained. (Selenium is the name of the tool used to perform the automation)

1. Create a folder named 'Profile Selenium' like this: "C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data\Profile Selenium"

2. Open Chrome manually using the profile you already configured in your script. You can do this using Windows Run or Command Prompt:
```
chrome.exe --user-data-dir="C:\Users\YOUR_USER\AppData\Local\Google\Chrome\User Data\Profile Selenium"
```
-Important: Close all Chrome windows before running this command to avoid instance conflicts.

3. Log in to Whatssapp Web
-Log in by scannong the QR Code.
-Check if you are authenticated and that the site maintains the session even after closing the tab.

## Usage
1. Run the script `main.py`.
   ```
   python main.py
   ```
2. Enter the following information:
   - File name (without extension) of the CSV file containing client data.
   - Three message parts: greeting, main message body, and closing message.
3. The program will load the client data from the CSV file and send personalized messages to each contact.
4. Monitor the progress and check for any errors or invalid phone numbers.
5. Once the process is complete, a report will be displayed with the number of messages sent and any invalid phone numbers encountered.

## Dependencies
- Python 3.x
- Selenium
- Chrome WebDriver
- Pandas

## Credits
- [Selenium](https://www.selenium.dev/) - Web browser automation tool.
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/) - WebDriver for Google Chrome.
- [Pandas](https://pandas.pydata.org/) - Python library for data manipulation and analysis.

## Disclaimer
<span style="font-size:12pt">This project was created for educational purposes only. Automating message sending on WhatsApp may violate the platform's terms of service and can potentially lead to account suspension or other consequences. The creators of this project do not endorse or encourage the unauthorized use of automated messaging tools on any platform. Users are advised to use this project responsibly and in compliance with applicable laws and regulations.</span>

---
