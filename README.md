# Web scraping project for link validation

![Banner](assets/media/Banner-LV.png)

## Define Project Scope:

- Check the validity and accessibility of URLs within a dataset or a web application.

### Project Objectives:

- Check that all links point to existing resources and are not broken or outdated.

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

## Wireframe

![Wireframe - Mobile](assets/media/Wireframe-mobile.png)

## Possible features

Search Functionality
Scraping and Data Retrieval
Filtering and Sorting
User Interface
Alerts and Notifications
Data Visualization

## Data Sources

- Wikpedia

## Data to Scrape

- Links

## Tools

- Requests
- Beautiful Soup
- Selenium
- Pandas
- Matplotlib or Seaborn
- Flask or Django
- Scrapy

## Implementation

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

## Credits

- [Web Scraping with Python and BeautifulSoup is THIS easy! - Tom's Tech Academy](https://www.youtube.com/watch?v=nBzrMw8hkmY)
- [Banner - Canva AI](https://www.canva.com)
- [The Best Websites to Practice Your Web Scraping Skills in 2024 - Proxyway](https://proxyway.com/guides/best-websites-to-practice-your-web-scraping-skills)
