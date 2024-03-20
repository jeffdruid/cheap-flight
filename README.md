# Web scraping project for link validation

![Banner](assets/media/Banner-LV.png)

## Introduction

The Link-Validator Tool is a Python application that allows users to scrape a webpage and validate all the links found within it. It performs checks for various link attributes, including URL validity, HTTP status codes, and the presence of Aria labels. The tool is especially useful for web developers, content managers, and SEO specialists who need to ensure the quality and integrity of hyperlinks on their websites.

## Table of Contents

1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
   - [Python](#python)
   - [BeautifulSoup](#beautifulsoup)
   - [Requests](#requests)
   - [Google Sheets API](#google-sheets-api)
   - [URLParse Import](#urlparse-import)
   - [pandas](#pandas)
   - [tqdm](#tqdm)
   - [Colorama](#colorama)
   - [os](#os)
   - [webbrowser](#webbrowser)
3. [User Stories](#user-stories)
4. [Wireframe](#wireframe)
5. [Features](#features)
   - [Scraping and Validation](#scraping-and-validation)
   - [Google Sheets Integration](#google-sheets-integration)
   - [Interactive Command-Line Interface (CLI)](#interactive-command-line-interface-cli)
   - [Color-Coded Output](#color-coded-output)
   - [Error Handling](#error-handling)
   - [Progress Indicator](#progress-indicator)
   - [Reporting](#reporting)
   - [GitHub Integration](#github-integration)
6. [Troubleshooting](#troubleshooting)
7. [Testing](#testing)
   - [Validator Testing](#validator-testing)
     - [Python](#python)
   - [Manual Testing](#manual-testing)
     - [Acceptance Test](#acceptance-test)
     - [Testing with invalid URLs](#testing-with-invalid-urls)
     - [Testing with various types of links (internal, external, anchor links)](#testing-with-various-types-of-links-internal-external-anchor-links)
     - [Testing with URLs requiring authentication](#testing-with-urls-requiring-authentication)
     - [Testing the Google Sheets integration functionality](#testing-the-google-sheets-integration-functionality)
8. [Bugs](#bugs)
   - [Fixed Bugs](#fixed-bugs)
9. [UI Improvements](#ui-improvements)
10. [Future Improvements](#future-improvements)
11. [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
12. [Deployment](#deployment)
    - [Cloning & Forking](#cloning--forking)
    - [Local Deployment](#local-deployment)
    - [Remote Deployment](#remote-deployment)
13. [Credits](#credits)
    - [Source Code](#source-code)
    - [Icons](#icons)
    - [Images](#images)
    - [Useful links](#useful-links)

## Technologies Used

- Python
- BeautifulSoup
- Requests
- Google Sheets API
- URLParse Import
- pandas
- tqdm
- colorama
- os
- webbrowser

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

- The URLParse import provides functions for parsing URLs into their components and joining URL components to form absolute URLs.

- Example Usage:

  ```bash
  from urllib.parse import urljoin, urlparse
  ```

- Explanation:

  - <b>urljoin</b>: Function for joining a base URL with another URL component to form an absolute URL.
  - <b>urlparse</b>: Function for parsing URLs into their components.

### pandas

- pandas is a powerful Python library for data manipulation and analysis. It provides data structures and functions designed to make working with structured data fast, easy, and expressive.

- Example Usage in the Code:

  ```bash
  import pandas as pd

  # Reading a CSV file into a pandas DataFrame
  df = pd.read_csv('data.csv')

  # Performing operations on the DataFrame
  df_filtered = df[df['column'] > 10]

  # Writing the modified DataFrame back to a CSV file
  df_filtered.to_csv('filtered_data.csv', index=False)
  ```

- Explanation:
  - In this example, pandas is imported as pd for convenience.
  - The read_csv() function is used to read data from a CSV file into a pandas DataFrame.
  - Various operations, such as filtering rows based on a condition, can be performed on the DataFrame.
  - The modified DataFrame can be written back to a CSV file using the to_csv() function.

### tqdm

- tqdm is a Python library that provides a fast, extensible progress bar for loops and other iterative processes. It offers a simple way to visualize the progress of tasks, making it easier to monitor long-running operations.

- Example Usage in the Code:

  ```bash
  from tqdm import tqdm

  # Iterating over a range with tqdm
  for i in tqdm(range(100)):
      # Perform some task here
      pass

  ```

- Explanation:
  - In this example, tqdm is imported to visualize the progress of a loop.
  - The tqdm() function wraps the iterable (in this case, range(100)) and displays a progress bar as the loop iterates.
  - Inside the loop, tasks are performed, and tqdm updates the progress bar accordingly.

### Colorama

- colorama is a Python library that makes it easy to add ANSI colors and styles to terminal output. It provides cross-platform support for colored text, allowing developers to create visually appealing command-line interfaces.

- Example Usage in the Code:

  ```bash
  import colorama
  from colorama import Fore, Back, Style

  # Initialize colorama
  colorama.init()

  # Print colored text
  print(Fore.RED + 'Error: Something went wrong!' + Style.RESET_ALL)
  ```

- Explanation:
  - In this example, colorama is imported to add color to terminal output.
  - The init() function is called to initialize colorama and set up the necessary environment variables.
  - ANSI color codes from colorama's Fore and Style modules are used to change the text color.
  - Style.RESET_ALL is used to reset the text color to the default after printing.

### os

- The os module in Python provides a way to interact with the operating system. It offers functions for performing tasks such as file operations, directory manipulation, and process management.

- Example Usage in the Code:

  ```bash
  import os

  # Get the current working directory
  cwd = os.getcwd()
  print('Current directory:', cwd)

  # List files in a directory
  files = os.listdir(cwd)
  print('Files in current directory:', files)
  ```

- Explanation:
  - In this example, os is imported to perform operating system-related tasks.
  - The getcwd() function is used to get the current working directory.
  - listdir() is used to list the files in the current working directory.

### webbrowser

- The webbrowser module in Python provides a high-level interface for displaying web-based documents to users. It allows Python scripts to open web browsers and display web pages, URLs, and HTML documents.

- Example Usage in the Code:

  ```bash
  import webbrowser

  # Open a web page in the default browser
  webbrowser.open('https://example.com')

  # Open a specific browser with a URL
  webbrowser.get('firefox').open_new_tab('https://example.com')
  ```

- Explanation:

  - In this example, webbrowser is imported to interact with web browsers.
  - The open() function opens the specified URL in the default web browser.
  - get() allows selecting a specific browser (e.g., Firefox) and opening a URL in a new tab using open_new_tab().

## User stories

| As a user...                                                                                                                             | I know I'm done when...                                   |
| ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- |
| I want to be able to input a URL so that I can validate its links.                                                                       | I see a prompt or interface to enter the URL              |
| I want to receive a list of all links found on the provided URL so that I can review them.                                               | I see a list of links displayed                           |
| I want to see the status of each link (valid or broken) so that I can assess the health of the website.                                  | I see each link marked as valid or broken                 |
| I want the tool to handle different types of links (internal, external, anchor links) so that I can validate any type of URL.            | I can validate internal, external, and anchor links       |
| I want the tool to handle redirects and follow them to the final destination so that I can accurately determine the status of each link. | I see the final destination status of each link           |
| I want to see a progress indicator while the tool is scanning the webpage so that I know it's working.                                   | I see a visual indicator or message showing progress      |
| I want the tool to provide detailed error messages for broken links so that I can understand why they failed.                            | I receive clear messages explaining why links failed      |
| I want the tool to be easy to use with a simple command-line interface so that I can quickly validate URLs without any hassle.           | I can easily run the tool from the command line           |
| I want the tool to generate a report summarizing the results of the link validation process so that I can easily share it with others.   | I receive a summary report of the link validation process |

## Wireframe

- TODO - Add flow chart instead of wireframes
  ![Wireframe - Mobile](assets/media/Wireframe-mobile.png)

## Features

- TODO - ADD screenshots

### Scraping and Validation

- Scrapes a webpage and validates all links found, checking for broken links, missing Aria labels, and more.

### Google Sheets Integration

- Stores link validation results in a Google Sheets document for easy access and sharing.

### Interactive Command-Line Interface (CLI)

- Provides a user-friendly CLI with menu options for different operations and displays results in real-time.

### Color-Coded Output

- Utilizes color-coded output for easy identification of link status (valid, invalid, etc.).

### Error Handling

- Implements robust error handling to handle various scenarios gracefully.

### Progress Indicator

- Displays a progress indicator during the link validation process to indicate the status of the operation.

### Reporting

- Generates a comprehensive report summarizing the results of the link validation process, including statistics and detailed information about broken links.

### GitHub Integration

- Provides a direct link to the project's GitHub repository for additional information and contributions.

## Troubleshooting

- TODO

## Testing

### Manual Testing

#### Acceptance Test

- Test Scenario: User inputs a valid URL and initiates the link validation process.

- Test Steps:

  - Open the command-line interface (CLI).
  - Run the Link-Validator Tool by executing the appropriate command (python run.py).
  - Enter a valid URL when prompted.
  - Verify that the tool starts validating the links found on the provided URL.
  - Verify that the tool displays progress indicators or messages during the validation process.
  - Verify that the tool generates a summary report of the link validation process upon completion.
  - Expected Result: The Link-Validator Tool successfully scrapes the webpage, validates all links, and generates a comprehensive report with accurate results.

- This acceptance test ensures that the core functionality of the Link-Validator Tool, which includes inputting a URL, validating links, and generating a report, functions as expected.

TODO - Add more test scenarios

#### Testing with invalid URLs

#### Testing with various types of links (internal, external, anchor links)

#### Testing with URLs requiring authentication

#### Testing the Google Sheets integration functionality

### Validator Testing

- TODO

#### Python test

- TODO

## Setup

- If you want to deploy the Link-Validator Tool locally for testing or development purposes, follow these steps:

### Prerequisites

Before running the Link-Validator Tool, ensure you have the following installed:

- Python 3.x
- pip package manager
- Google Account (for Google Sheets integration)

### Installation

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

### Usage

To run the Link-Validator Tool, execute the following command in your terminal:

```bash
python run.py
```

## Deployment

### Cloning & Forking

#### Cloning

- To clone this repository to your local machine, use the following command:

  ```bash
  git clone https://github.com/yourusername/link-validator.git
  ```

#### Forking

- To fork this repository, click the Fork button in the upper right corner of the repository page.

### Local Deployment

- To deploy this project locally, follow the installation instructions provided in the Setup section.

### Remote Deployment (Heroku)

1. Create a Heroku Account
   If you haven't already, sign up for a free account on [Heroku](https://signup.heroku.com/)

2. Install Heroku CLI
   Download and install the Heroku CLI for your operating system.

3. Login to Heroku
   Open a terminal or command prompt and login to your Heroku account using the following command:

```bash
heroku login
```

Follow the prompts to enter your Heroku credentials.

4. Prepare Your Application
   Ensure your application is ready for deployment to Heroku:

- Make sure your application has a requirements.txt file listing all dependencies.
- Include a Procfile in the root directory of your project. This file specifies the commands that Heroku should use to run your application.
- If your application requires any environment variables, ensure they are properly configured.

5. Initialize Git Repository

- If your project is not already a Git repository, initialize one:

```bash
git init
git add .
git commit -m "Initial commit"
```

6. Create a Heroku App
   Create a new Heroku app using the Heroku CLI:

```bash
heroku create your-app-name
```

Replace your-app-name with a unique name for your Heroku app.

7. Deploy Your Application
   Deploy your application to Heroku using Git:

```bash
git push heroku main
```

Replace main with the name of your main branch if it's different (e.g., master).

8. Open Your Application
   Once the deployment is complete, you can open your application in the browser using the following command:

```bash
heroku open
```

- This will open your application in the default web browser.
- Your Python application should now be deployed and running on Heroku. You can access it using the provided Heroku URL or custom domain if configured.

## Bugs

- TODO

### Fixed Bugs

- TODO

## UI Improvements

- TODO

## Futures Improvements

- **Improved Link Validation Algorithm**: Enhance the link validation algorithm to handle edge cases more effectively and accurately detect various types of broken links.
- **Enhanced User Interface**: Develop a graphical user interface (GUI) using a framework like PyQt or Tkinter to provide a more intuitive and visually appealing experience for users.
- **Parallel Processing**: Implement parallel processing techniques to speed up the link validation process, allowing the tool to handle large websites more efficiently.
- **Customizable Reporting**: Allow users to customize the format and content of the link validation report, including options to export data in different formats (e.g., CSV, PDF).
- **Integration with More External Services**: Integrate with additional external services and APIs to enhance functionality, such as integration with popular CMS platforms or SEO analysis tools.
- **Scheduled Scans**: Add support for scheduled scans or automated monitoring of websites, enabling users to receive regular reports on the status of their links.
- **Browser Extension**: Develop a browser extension that users can install to perform link validation directly within their web browsers, simplifying the validation process.
- **Advanced Configuration Options**: Provide advanced configuration options for users to customize the link validation process, such as specifying timeout values or configuring custom headers for requests.
- **Error Handling Enhancements**: Improve error handling mechanisms to gracefully handle unexpected errors and provide more informative error messages to users.
- **Internationalization (i18n)**: Implement support for multiple languages to make the tool accessible to users from different regions and language preferences.

## Credits

- TODO

### Source Code

- TODO
- [Link-Test Github](https://github.com/jeffdruid/link-test)

#### Images

-TODO

#### Useful links

- TODO
- [Link-Test Page](https://jeffdruid.github.io/link-test/)
- [Web Scraping with Python and BeautifulSoup is THIS easy! - Tom's Tech Academy](https://www.youtube.com/watch?v=nBzrMw8hkmY)
- [Banner - Canva AI](https://www.canva.com)
- [The Best Websites to Practice Your Web Scraping Skills in 2024 - Proxyway](https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills)
