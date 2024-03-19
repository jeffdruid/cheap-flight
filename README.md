# Web scraping project for link validation

![Banner](assets/media/Banner-LV.png)

## Introduction

The Link-Validator Tool is a Python application that allows users to scrape a webpage and validate all the links found within it. It performs checks for various link attributes, including URL validity, HTTP status codes, and the presence of Aria labels. The tool is especially useful for web developers, content managers, and SEO specialists who need to ensure the quality and integrity of hyperlinks on their websites.

## Table of Contents

1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [User Stories](#user-stories)
4. [Wireframe](#wireframe)
5. [Features](#features)
   - [Header](#header)
6. [Troubleshooting](#troubleshooting)
7. [Testing](#testing)
   - [Validator Testing](#validator-testing)
     - [Python](#python)
   - [Accessibility](#accessibility)
   - [Lighthouse](#lighthouse)
   - [Responsiveness](#responsiveness)
   - [Manual Testing](#manual-testing)
     - [Cross-browser Compatibility](#cross-browser-compatibility)
     - [Responsiveness and Device Compatibility](#responsiveness-and-device-compatibility)
     - [Link Validation](#link-validation)
     - [Text and Font Readability](#text-and-font-readability)
     - [Acceptance Test](#acceptance-test)
     - [Desktop](#desktop)
     - [Tablet](#tablet)
     - [Mobile](#mobile)
8. [Bugs](#bugs)
   - [Fixed Bugs](#fixed-bugs)
9. [UI Improvements](#ui-improvements)
10. [Future Improvements](#future-improvements)
11. [Deployment](#deployment)
    - [Cloning & Forking](#cloning--forking)
    - [Local Deployment](#local-deployment)
    - [Remote Deployment](#remote-deployment)
12. [Credits](#credits)
    - [Source Code](#source-code)
    - [Icons](#icons)
    - [Images](#images)
    - [Useful links](#useful-links)

## User stories

- TODO

## Features

- TODO - ADD screenshots
- **Scraping and Validation**: Scrapes a webpage and validates all links found, checking for broken links, missing Aria labels, and more.
- **Google Sheets Integration**: Stores link validation results in a Google Sheets document for easy access and sharing.
- **Interactive Command-Line Interface (CLI)**: Provides a user-friendly CLI with menu options for different operations and displays results in real-time.
- **Color-Coded Output**: Utilizes color-coded output for easy identification of link status (valid, invalid, etc.).
- **Error Handling**: Implements robust error handling to handle various scenarios gracefully.
- **GitHub Integration**: Provides a direct link to the project's GitHub repository for additional information and contributions.

## Prerequisites

Before running the Link-Validator Tool, ensure you have the following installed:

- Python 3.x
- pip package manager
- Google Account (for Google Sheets integration)

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/link-validator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd link-validator
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Obtain Google Sheets API credentials:
   - Visit the [Google Developers Console](https://console.developers.google.com/).
   - Create a new project.
   - Enable the Google Sheets API for your project.
   - Create service account credentials and download the JSON file.
   - Rename the JSON file to `creds.json` and place it in the project directory.

## Usage

To run the Link-Validator Tool, execute the following command in your terminal:

```bash
python run.py
```

## Wireframe

- TODO - Add flow chart instead of wireframes
  ![Wireframe - Mobile](assets/media/Wireframe-mobile.png)

## Technologies Used

### Python

- Python is a high-level programming language known for its simplicity and readability. It is widely used in web development, data analysis, artificial intelligence, and more. In the Link-Validator Tool, Python serves as the primary programming language for backend development.

      - Example Usage:

```bash
      import requests
      response = requests.get('https://example.com')
      print(response.status_code)
```

- Explanation:
  - In this example, Python's requests library is used to send an HTTP GET request to a URL (https://example.com).
  - The response object contains information about the HTTP response, including the status code.
  - The status_code attribute is accessed to print the status code of the response.

### BeautifulSoup

- BeautifulSoup is a Python library for parsing HTML and XML documents. It provides a simple interface for navigating and searching the parse tree, making it easy to extract data from web pages.

- Example Usage:

  ```bash
     from bs4 import BeautifulSoup

     html_doc = """

     <html><head><title>Example</title></head>
     <body><p>Hello, world!</p></body></html>
     """
     soup = BeautifulSoup(html_doc, 'html.parser')
     print(soup.p.text)
  ```

- Explanation:
  - In this example, BeautifulSoup is used to parse an HTML document (html_doc) and create a parse tree.
  - The html.parser is used as the parser for parsing the HTML document.
  - The soup.p.text expression extracts the text content of the first <p> tag found in the HTML document.

### Requests

- Requests is an elegant and simple HTTP library for Python, allowing you to send HTTP requests easily. It is commonly used for interacting with web APIs and fetching web pages.

  - Example Usage:

    ```bash
    import requests

    response = requests.get('https://api.example.com/data')
    data = response.json()
    print(data)
    ```

- Explanation:
  - Here, the requests.get() function is used to send an HTTP GET request to the specified URL (https://api.example.com/data).
  - The json() method is called on the response object to deserialize the JSON response content into a Python dictionary.
  - Finally, the content of the response is printed, which typically represents data obtained from the API.

### Google Sheets API

- The Google Sheets API allows developers to read, write, and format data in Google Sheets. It enables integration with Google Sheets, enabling applications to update spreadsheet data programmatically.

- Example Usage:

  ```bash
  import gspread
  from oauth2client.service_account import ServiceAccountCredentials

  # Define the scope and credentials

  scope = ['https://www.googleapis.com/auth/spreadsheets']
  creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

  # Authorize the client

  client = gspread.authorize(creds)

  # Open a spreadsheet by its title

  sheet = client.open('Example Spreadsheet')

  # Select a worksheet

  worksheet = sheet.get_worksheet(0)

  # Update a cell

  worksheet.update_cell(1, 1, 'New Value')
  ```

- Explanation:
  - In this example, the Google Sheets API is used to interact with a Google Sheets spreadsheet.
  - ServiceAccountCredentials are used to authenticate the application using a service account and credentials stored in a JSON key file.
  - The gspread library is used to authorize the client and interact with the Google Sheets API.
  - A spreadsheet titled 'Example Spreadsheet' is opened, and a specific worksheet is selected.
  - The update_cell() method is used to update the value of a cell in the worksheet.

### URLParse Import

- TODO - Definition

- Example Usage:

  ```bash
  from urllib.parse import urljoin, urlparse
  ```

- Explanation:

  - <b>urljoin</b>: Function for joining a base URL with another URL component to form an absolute URL.
  - <b>urlparse</b>: Function for parsing URLs into their components.

- TODO - add the other libraries
  - import pandas as pd
  - from tqdm import tqdm
  - import colorama
  - from colorama import Back, Fore, Style
  - import os
  - import webbrowser

## Troubleshooting

- TODO

## Testing

- TODO

### Validator Testing

- TODO

#### Python test

- TODO

## Implementation

- TODO remove

### Data Preprocessing:

- Preprocessing the data to extract and clean the URLs.
- Ensure that URLs are properly formatted and free of any extra characters or whitespace.

### URL Validation:

- Use Python libraries like `validators` or `urllib.parse` to validate the syntax and structure of URLs.
- Check if the URLs conform to standards such as HTTP/HTTPS protocols, domain names, and path formats.

### Link Checking:

- Use Python libraries like requests to send HTTP requests to each URL and check the response status.
- Check for common HTTP status codes such as 200 (OK), 404 (Not Found), 403 (Forbidden), etc.
- Handle cases where URLs are redirected or have other issues such as timeout or connection errors.

### Error Handling:

- Implement error handling mechanisms to gracefully handle exceptions and errors encountered during link validation.
- Log errors and invalid URLs for further analysis or manual inspection.

### Reporting:

- Generate a report summarizing the results of the link validation process.
- Include statistics such as the number of valid links, broken links, redirection, and errors encountered.

### Automated Testing:

- Integrate link validation as part of automated testing suites to continuously monitor the health of URLs in your project.
- Use testing frameworks like pytest or unittest to write test cases for link validation.

### Integration with Web Applications:

- Integrate link validation as a feature for users to check the validity of URLs.
- Provide feedback to users about the status of each URL, such as indicating whether it's valid, broken, or redirected.

## Bugs

- TODO

### Fixed Bugs

- TODO

## UI Improvements

- TODO

## Futures Improvements

- TODO

## Credits

- TODO

### Source Code

- TODO
- TODO - Add test source code [Link-Test](github.com)

#### Images

-TODO

#### Useful links

- TODO

- [Web Scraping with Python and BeautifulSoup is THIS easy! - Tom's Tech Academy](https://www.youtube.com/watch?v=nBzrMw8hkmY)
- [Banner - Canva AI](https://www.canva.com)
- [The Best Websites to Practice Your Web Scraping Skills in 2024 - Proxyway](https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills)
