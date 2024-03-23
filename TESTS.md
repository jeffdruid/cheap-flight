# README for Link-Validator Tool Testing

## [Back to Link-Validator Tool README](README.md)

### Link-Validator Tool Testing

- The testing results were documented in this file to provide an overview of the testing process and outcomes.

### Manual Testing

- **Manual testing** was performed to validate the functionality and user experience of the Link-Validator Tool.

#### Table of Contents

- [Acceptance Test](#acceptance-test)
- [Application Start-Up Tests](#application-start-up-tests)
- [Main Menu](#main-menu)
- [Option 1 - Scrape and Validate Links](#option-1---scrape-and-validate-links)
- [Option 2 - Display All Links Scraped](#option-2---display-all-links-scraped)
- [Option 3 - Display Links not Verified due to Connection Errors](#option-3---display-links-not-verified-due-to-connection-errors)
- [Option 4 - Display Links with Missing Aria Labels](#option-4---display-links-with-missing-aria-labels)
- [Option 5 - Display Broken Links](#option-5---display-broken-links)
- [Option 6 - Display a Summary of Findings](#option-6---display-a-summary-of-findings)
- [Option 7 - Empty the Links Google Sheet](#option-7---empty-the-links-google-sheet)
- [Option 8 - Open Google Sheets](#option-8---open-google-sheets)
- [Option 9 - View Source Code on GitHub](#option-9---view-source-code-on-github)
- [Prompt to Continue or Exit](#prompt-to-continue-or-exit)

#### Acceptance Test

The following test scenarios were used to validate the Link-Validator Tool's functionality and user experience:

| Test Scenario                                              | Test Steps                                                                                                                                                                 | Expected Result                                                                                                                            |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| User inputs a valid URL and initiates link validation      | 1. Open the command-line interface (CLI).<br> 2. Run the Link-Validator Tool by executing the appropriate command (python run.py).<br> 3. Enter a valid URL when prompted. | The Link-Validator Tool successfully scrapes the webpage, validates all links, and generates a comprehensive report with accurate results. |
| User inputs an invalid URL and attempts to validate links  | Enter an invalid URL when prompted.                                                                                                                                        | The Link-Validator Tool detects the invalid URL and displays an error message indicating the issue.                                        |
| User validates a webpage containing various types of links | Enter a URL with internal, external, and anchor links when prompted.                                                                                                       | The Link-Validator Tool successfully validates internal, external, and anchor links found on the webpage.                                  |
| User validates a webpage that requires authentication      | Enter a URL that requires authentication when prompted.                                                                                                                    | The Link-Validator Tool successfully validates links on webpages that require authentication, ensuring accurate results.                   |
| User tests Google Sheets integration functionality         | Enter a URL to validate and choose to save results to Google Sheets.                                                                                                       | The Link-Validator Tool integrates with Google Sheets and saves the link validation results for easy access and sharing.                   |
| User tests color-coded output feature                      | Enter a URL to validate and observe the color-coded output.                                                                                                                | The Link-Validator Tool displays link validation results using color-coded output for easy identification and interpretation.              |
| User tests error handling mechanism                        | Enter a URL that triggers an error during validation.                                                                                                                      | The Link-Validator Tool handles errors during the validation process and displays clear error messages to guide users.                     |
| User tests trailing slashes in URLs                        | Enter a URL with a trailing slash when prompted.                                                                                                                           | The Link-Validator Tool accurately validates links on webpages with trailing slashes in the URL.                                           |
| User tests progress indicator feature                      | Enter a URL to validate and observe the progress indicator.                                                                                                                | The Link-Validator Tool provides a progress indicator to inform users about the status of the validation process.                          |
| User tests reporting functionality                         | Enter a URL to validate and choose to generate a report.                                                                                                                   | The Link-Validator Tool creates a comprehensive report summarizing the link validation results.                                            |
| User tests GitHub integration feature                      | Choose the option to view the GitHub repository.                                                                                                                           | The Link-Validator Tool integrates with GitHub and provides users with a direct link to the project repository for additional information. |
| User chooses to display all links scraped from webpage     | Select the option to display all links scraped from the last webpage.                                                                                                      | The Link-Validator Tool displays all links scraped from the last webpage.                                                                  |
| User chooses to view links with connection errors          | Select the option to view links with connection errors.                                                                                                                    | The Link-Validator Tool displays links that were not verified due to connection errors.                                                    |
| User chooses to display links with missing Aria labels     | Select the option to display links with missing Aria labels.                                                                                                               | The Link-Validator Tool displays links with missing Aria labels.                                                                           |
| User chooses to view broken links                          | Select the option to view broken links.                                                                                                                                    | The Link-Validator Tool displays broken links found during validation.                                                                     |
| User chooses to view a summary of findings                 | Select the option to view a summary of findings.                                                                                                                           | The Link-Validator Tool displays a summary of the link validation findings.                                                                |
| User chooses to empty the Google Sheet                     | Select the option to empty the Google Sheet.                                                                                                                               | The Link-Validator Tool clears all data stored in the Google Sheet.                                                                        |
| User chooses to open the Google Sheets                     | Select the option to open the Google Sheets.                                                                                                                               | The Link-Validator Tool opens the Google Sheets for viewing and management.                                                                |
| User chooses to view the source code on GitHub             | Select the option to view the source code on GitHub.                                                                                                                       | The Link-Validator Tool opens the GitHub repository in the default web browser for users to explore the source code.                       |

#### Application Start-Up Tests

| Test Number | Test                      | Test Data              | Expected Result                                                                             | Actual Result                                                                                     | Test Result |
| ----------- | ------------------------- | ---------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ----------- |
| 1           | Check Internet Connection | Internet connection    | Displays a colorful welcome message and menu options if an internet connection is available | Colorful welcome message displayed along with menu options if an internet connection is available | Pass        |
| 2           | Check Internet Connection | No internet connection | Program terminates with a connection error message                                          | Program terminated with a connection error message                                                | Pass        |

#### Main menu

| Test Number | Test                                 | Test Data              | Expected Result                                          | Actual Result                                          | Test Result |
| ----------- | ------------------------------------ | ---------------------- | -------------------------------------------------------- | ------------------------------------------------------ | ----------- |
| 1           | Main Menu Validation                 | Input " "              | Error message                                            | Error message displayed                                | Pass        |
| 2           | Main Menu Validation                 | Input "a"              | Error message                                            | Error message displayed                                | Pass        |
| 3           | Main Menu Validation                 | Input 20               | Error message                                            | Error message displayed                                | Pass        |
| 4           | Main Menu Validation                 | Input "$"              | Error message                                            | Error message displayed                                | Pass        |
| 5           | Main Menu Validation                 | Input 0                | Exits the program                                        | Program exited successfully                            | Pass        |
| 6           | Main Menu Validation                 | Input 1-9              | Displays the corresponding functionality menu            | Correct menu displayed for the entered option          | Pass        |
| 7           | Main Menu Validation                 | Input other characters | Error message                                            | Error message displayed                                | Pass        |
| 8           | Program termination by user (Ctrl+C) | Ctrl+C                 | Program terminates gracefully with a termination message | Program terminated gracefully with termination message | Pass        |

#### Option 1 - Scrape and Validate Links

| Test Number | Test                                                                         | Test Data                            | Expected Result                                                                                               | Actual Result                                                   | Test Result |
| ----------- | ---------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------- |
| 1           | User selects Option 1 and provides a valid URL                               | Valid URL                            | The tool scrapes the webpage, validates all links, and generates a comprehensive report with accurate results | Webpage scraped, links validated, and accurate report generated | Pass        |
| 2           | User selects Option 1 and provides an invalid URL                            | Invalid URL                          | The tool displays an error message indicating the invalid URL                                                 | Error message displayed indicating the invalid URL              | Pass        |
| 3           | User selects Option 1 but does not provide a URL                             | No URL provided                      | The tool prompts the user to enter a valid URL                                                                | Prompt displayed asking for a valid URL                         | Pass        |
| 4           | User cancels Option 1 selection                                              | Cancel selection                     | The tool returns to the main menu without any action                                                          | Returned to main menu without any action                        | Pass        |
| 5           | User selects Option 1 and enters a URL with no links                         | URL with no links                    | The tool completes validation with no links found                                                             | Validation completed with no links found                        | Pass        |
| 6           | User selects Option 1 and enters a URL with only internal links              | URL with internal links              | The tool validates internal links only                                                                        | Internal links validated                                        | Pass        |
| 7           | User selects Option 1 and enters a URL with only external links              | URL with external links              | The tool validates external links only                                                                        | External links validated                                        | Pass        |
| 8           | User selects Option 1 and enters a URL with both internal and external links | URL with internal and external links | The tool validates both internal and external links                                                           | Both internal and external links validated                      | Pass        |
| 9           | User selects Option 1 and enters a URL with anchor links only                | URL with anchor links                | The tool validates anchor links only                                                                          | Anchor links validated                                          | Pass        |
| 10          | User selects Option 1 and enters a URL with mixed link types                 | URL with mixed link types            | The tool validates all types of links found on the webpage                                                    | All types of links validated                                    | Pass        |

#### Option 2 - Display All Links Scraped

| Test Number | Test                                                      | Test Data | Expected Result                                       | Actual Result                               | Test Result |
| ----------- | --------------------------------------------------------- | --------- | ----------------------------------------------------- | ------------------------------------------- | ----------- |
| 1           | User selects Option 2 when no links have been scraped yet | NA        | The tool displays a message indicating no links found | Message displayed indicating no links found | Pass        |
| 2           | User selects Option 2 after scraping links from a webpage | NA        | The tool displays all links scraped from the webpage  | All links from the last webpage displayed   | Pass        |
| 3           | User cancels Option 2 selection                           | NA        | The tool returns to the main menu                     | Returned to main menu without any action    | Pass        |

#### Option 3 - Display Links not Verified due to Connection Errors

| Test Number | Test                                                          | Test Data | Expected Result                                                | Actual Result                                       | Test Result |
| ----------- | ------------------------------------------------------------- | --------- | -------------------------------------------------------------- | --------------------------------------------------- | ----------- |
| 1           | User selects Option 3 to display links with connection errors | N/A       | Displays links that were not verified due to connection errors | Links with connection errors displayed              | Pass        |
| 2           | No links with connection errors found                         | N/A       | Displays an error message indicating no connection errors      | Error message indicating no connection errors found | Pass        |
| 3           | No links scraped from the last webpage                        | N/A       | Displays an error message indicating no links found            | Error message indicating no links found displayed   | Pass        |

#### Option 4 - Display Links with Missing Aria Labels

| Test Number | Test                                                            | Test Data | Expected Result                                      | Actual Result                              | Test Result |
| ----------- | --------------------------------------------------------------- | --------- | ---------------------------------------------------- | ------------------------------------------ | ----------- |
| 1           | User selects Option 4 to display links with missing Aria labels | N/A       | Displays links with missing Aria labels              | Links with missing Aria labels displayed   | Pass        |
| 2           | User selects Option 4 to display links with missing Aria labels | N/A       | Displays a message indicating no missing Aria labels | No missing Aria labels found               | Pass        |
| 3           | User selects Option 4 when Google Sheets is empty               | N/A       | Displays an error message indicating no data         | Error message indicating no data displayed | Pass        |

#### Option 5 - Display Broken Links

| Test Number | Test                                                                          | Test Data | Expected Result                               | Actual Result                              | Test Result |
| ----------- | ----------------------------------------------------------------------------- | --------- | --------------------------------------------- | ------------------------------------------ | ----------- |
| 1           | User selects Option 5 to display broken links (broken links count > 0)        | N/A       | Displays all broken links                     | Broken links displayed                     | Pass        |
| 2           | User selects Option 5 when no broken links are found (broken links count = 0) | N/A       | Displays a message indicating no broken links | No broken links message displayed          | Pass        |
| 3           | User selects Option 5 when Google Sheets is empty                             | N/A       | Displays an error message indicating no data  | Error message indicating no data displayed | Pass        |

#### Option 6 - Display a Summary of Findings

| Test Number | Test                                              | Test Data | Expected Result                | Actual Result                 | Test Result |
| ----------- | ------------------------------------------------- | --------- | ------------------------------ | ----------------------------- | ----------- |
| 1           | User selects Option 6 to display summary          | N/A       | Displays a summary of findings | Summary of findings displayed | Pass        |
| 2           | User selects Option 6 when Google Sheets is empty | N/A       | Displays an error message      | Error message displayed       | Pass        |

#### Option 7 - Empty the Links Google Sheet

| Test Number | Test                                                         | Test Data | Expected Result                                  | Actual Result                                | Test Result |
| ----------- | ------------------------------------------------------------ | --------- | ------------------------------------------------ | -------------------------------------------- | ----------- |
| 1           | User selects Option 7 to empty the Google Sheet              | N/A       | Prompts the user for confirmation                | User prompted for confirmation               | Pass        |
| 2           | User selects Option 7 and opts to empty the Google Sheet     | 'y'       | Google Sheet is emptied after user confirmation  | Google Sheet emptied after user confirmation | Pass        |
| 3           | User selects Option 7 and opts not to empty the Google Sheet | 'n'       | Google Sheet not emptied after user confirmation | Google Sheet not emptied after confirmation  | Pass        |

#### Option 8 - Open Google Sheets

| Test Number | Test                                                                 | Test Data | Expected Result                               | Actual Result                           | Test Result |
| ----------- | -------------------------------------------------------------------- | --------- | --------------------------------------------- | --------------------------------------- | ----------- |
| 1           | User selects Option 8 to open Google Sheets                          | N/A       | Opens the Google Sheets in the web browser    | Google Sheets not opened in the browser | Fail        |
| 4           | User unable to open Google Sheets and opts to view the link provided | N/A       | Google Sheets link provided for manual access | Google Sheets link displayed            | Pass        |

#### Option 9 - View Source Code on GitHub

| Test Number | Test                                                   | Test Data | Expected Result                                   | Actual Result                                   | Test Result |
| ----------- | ------------------------------------------------------ | --------- | ------------------------------------------------- | ----------------------------------------------- | ----------- |
| 1           | User selects Option 9 to view source code on GitHub    | NA        | Opens the GitHub repository in the web browser    | GitHub repository not opened in the web browser | Fail        |
| 2           | User selects Option 9 and the GitHub link doesn't open | NA        | Displays a message with the GitHub repository URL | GitHub repository URL display link              | Pass        |

#### Prompt to Continue or Exit

- The tool prompts the user to continue or exit after completing an operation.

| Test Number | Test                                                       | Test Data | Expected Result                                      | Actual Result                                       | Test Result |
| ----------- | ---------------------------------------------------------- | --------- | ---------------------------------------------------- | --------------------------------------------------- | ----------- |
| 1           | User selects an option and chooses to continue             | 'y'       | The tool returns to the main menu                    | Returned to main menu without any action            | Pass        |
| 2           | User selects an option and chooses to exit                 | 'n'       | The tool terminates with a goodbye message           | Program terminated with a goodbye message           | Pass        |
| 3           | User provides an invalid choice during the continue prompt | 'x'       | The tool displays an error message and prompts again | Error message displayed, prompting for choice again | Pass        |
