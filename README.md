# Automessager WG-Gesucht

This Python script automates the process of sending application messages to listings on WG-Gesucht.de, a popular platform for finding shared apartments in Germany. It is designed to streamline the application process by automatically identifying new listings that match specified criteria and sending personalized messages to them.

## Features

    Automated scanning of WG-Gesucht listings based on user-defined search parameters.

    Personalized message generation using customizable templates.

    Automated submission of application messages to selected listings.

    Logging of sent messages and application statuses for tracking purposes.

## Requirements

    Python 3.6 or higher

    Selenium WebDriver

    Geckodriver (for Firefox)

    A WG-Gesucht account
    GitHub

## Installation

    Clone the repository:

    git clone https://github.com/wmbm/automessager_WG_gesucht.git
    cd automessager_WG_gesucht

    Create and activate a virtual environment (optional but recommended):

    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    Install the required packages:

    pip install -r requirements.txt

    Download and install Geckodriver and ensure it is in your system's PATH.

## Usage

    Configure your search parameters and message templates in a configuration file or directly within the script.

    Run the script:

    python main.py

    The script will log in to your WG-Gesucht account, search for new listings matching your criteria, and send application messages using your templates.

## Notes

    Ensure that your WG-Gesucht account credentials are stored securely and not hard-coded into the script.

    Be mindful of WG-Gesucht's terms of service and avoid sending excessive or spammy messages.
