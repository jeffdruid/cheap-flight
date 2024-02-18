Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **March 14, 2023**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!

# Web scraping project for link validation

![Banner](assets/media/Banner-LV.png)

## Define Project Scope:

- Check the validity and accessibility of URLs within a dataset or a web application.

### Project Objectives:

- Check that all links point to existing resources and are not broken or outdated.

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
