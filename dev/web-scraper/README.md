# Ethical Hacker Web Scraper - Advanced

This project contains both a Python and a C++ version of a web scraper designed for ethical web scraping and security testing. The scraper extracts information from websites, detects malicious content, checks for spam links, and allows saving the results in CSV format.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Legal Disclaimer](#legal-disclaimer)
- [Safety Information](#safety-information)
- [Python Version Setup](#python-version-setup)
  - [Dependencies](#python-dependencies)
  - [Setup Steps](#python-setup-steps)
  - [Running the Python Application](#running-the-python-application)
- [C++ Version Setup](#cpp-version-setup)
  - [Dependencies](#cpp-dependencies)
  - [Setup Steps](#cpp-setup-steps)
  - [Running the C++ Application](#running-the-cpp-application)

## Overview

This tool is designed for ethical hackers, security testers, and web scraping enthusiasts. It allows users to scrape website data and analyze it for malicious content, such as phishing attempts, spam, or dangerous scripts. It is essential to use this tool ethically and within the boundaries of legal frameworks.

## Features

- Scrapes websites for titles, links, paragraphs, and images.
- Detects malicious content like spam links and harmful JavaScript.
- Allows saving the scraped data to a CSV file.
- Checks for robots.txt to ensure compliance with the website’s scraping policies.

## Legal Disclaimer

By using this tool, you agree to the following:

1. **Ethical Use**: This tool is intended for ethical and legal use only. Always ensure you have permission to scrape a website and respect its robots.txt file.
2. **Compliance with Laws**: The user must comply with all local, national, and international laws, including data protection and privacy regulations (e.g., GDPR, CCPA). Unauthorized web scraping can violate terms of service agreements and may result in legal consequences.
3. **Responsibility**: The creator of this tool is not responsible for any actions taken using this tool. It is the responsibility of the user to ensure that their usage complies with applicable laws and ethical standards.

## Safety Information

1. **Website Permissions**: Always check a website’s `robots.txt` to ensure you are allowed to scrape it.
2. **Rate Limiting**: Avoid sending too many requests in a short period to prevent overloading the target server. Implement delays between requests to comply with ethical scraping practices.
3. **Data Privacy**: Be mindful of the data you scrape. Do not collect or distribute sensitive personal information without proper authorization.
4. **Malicious Content**: This tool can detect malicious content, but it is important to use this information responsibly and within legal boundaries.

## Python Version Setup

### Dependencies

To run the Python version of this tool, you need to install the following Python packages:

- **requests**: For making HTTP requests to websites.
- **beautifulsoup4**: For parsing HTML data.
- **selenium**: For automating web browsers and interacting with dynamic content.
- **PyQt6**: For creating the GUI.

You can install the dependencies using `pip`:

```bash
pip install requests beautifulsoup4 selenium PyQt6
```

Additionally, you need to download the appropriate WebDriver for Selenium. For example, if you're using Chrome, download the [ChromeDriver](https://sites.google.com/chromium.org/driver/).

### Setup Steps

1. **Install Python**: Ensure Python 3.6+ is installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).
2. **Install Dependencies**: Run the following command to install the required Python libraries:

    ```bash
    pip install requests beautifulsoup4 selenium PyQt6
    ```

3. **Download WebDriver**: Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome) and ensure it's in your system's PATH or specify the full path in the code.

### Running the Python Application

1. **Run the Script**: After setting up Python and installing dependencies, run the Python application using:

    ```bash
    python web_scraper.py
    ```

2. **Interface**: A GUI window will appear where you can input the URL of the website you want to scrape. Click the "Scrape Website" button to start scraping, and view the results in the table.

## C++ Version Setup

### Dependencies

To run the C++ version of the tool, you need the following dependencies:

- **C++ Compiler**: Ensure you have a C++ compiler installed (e.g., GCC, Clang, MSVC).
- **CMake**: For managing the build process.
- **libcurl**: For making HTTP requests.
- **BeautifulSoup++**: A C++ library for HTML parsing (or you can use other libraries for HTML parsing).

### Setup Steps

1. **Install C++ Compiler**: Ensure you have a C++ compiler installed on your system (e.g., GCC for Linux, MSVC for Windows).
2. **Install libcurl**: Install libcurl to handle HTTP requests.

    - On **Ubuntu**:

        ```bash
        sudo apt-get install libcurl4-openssl-dev
        ```

    - On **Windows**: Download the [libcurl Windows binaries](https://curl.haxx.se/download.html) and add them to your system's PATH.

3. **Download BeautifulSoup++**: Download the necessary C++ library for HTML parsing or use alternatives (like `htmlcxx`, `gumbo`, etc.).

### Running the C++ Application

1. **Build the C++ Application**: Navigate to the project directory and run the build command (e.g., `make` or `cmake`):

    ```bash
    mkdir build
    cd build
    cmake ..
    make
    ```

2. **Run the Application**: After building, execute the compiled binary:

    ```bash
    ./web_scraper
    ```

3. **Interface**: The application will open a terminal-based interface for inputting the URL and performing scraping.