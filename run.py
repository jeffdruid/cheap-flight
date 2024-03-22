import os
import urllib.parse
import webbrowser
from urllib.parse import urljoin

import colorama
import gspread
import pandas as pd
import requests
from bs4 import BeautifulSoup
from colorama import Back, Fore, Style
from google.oauth2.service_account import Credentials
from tqdm import tqdm


class LinkValidator:
    """
    Initialize the LinkValidator class.
    """

    def __init__(self):
        # Constants
        self.RED = Fore.RED
        self.GREEN = Fore.GREEN
        self.YELLOW = Fore.YELLOW
        self.CYAN = Fore.CYAN
        self.MAGENTA = Fore.MAGENTA
        self.WHITE = Fore.WHITE
        self.BLACK = Fore.BLACK
        self.RESET = Style.RESET_ALL
        self.ERROR_MESSAGE = (
            self.RED
            + "\nNo links found. Please scrape a webpage first."
            + self.RESET
        )
        self.initialize_colorama()

        self.SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        # Google Sheets API credentials
        self.CREDS = Credentials.from_service_account_file("creds.json")
        self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
        self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
        self.SHEET = self.GSPREAD_CLIENT.open("LinkValidator")
        self.WORKSHEET = self.SHEET.sheet1

    def initialize_colorama(self):
        """
        Initialize colorama and set the color for the welcome message.
        """
        colorama.init()

        # Check internet connectivity
        if not self.check_internet_connection():
            print(
                self.RED
                + "\nError: No internet connection. Please"
                + " check your network connection and try again."
                + self.RESET
            )
            exit()

    def check_internet_connection(self):
        """
        Check internet connectivity.
        """
        try:
            requests.get("http://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False
        except requests.Timeout:
            print(
                "Connection timed out. Please check your"
                + " internet connection and try again later."
            )
            return False

    def print_welcome_message(self):
        """
        Print the welcome message for the Link-Validator Tool.
        """
        # Clear the console
        self.clear_console()
        print(
            Style.BRIGHT
            + Back.GREEN
            + Fore.WHITE
            + "\nWelcome to the Link-Validator Tool!\n"
            + self.RESET
            + self.YELLOW
            + "This tool allows you to scrape a webpage"
            + " and validate all the links."
            + self.RESET
        )

    def print_instructions(self):
        """
        Display the instructions for using the Link-Validator Tool.
        """

        print(self.MAGENTA + "\nMenu options:" + self.RESET)
        print(self.CYAN + "-" * 63)
        print("1. Scrape and Validate Links from a Webpage")
        print("-" * 63)
        print(self.YELLOW + "Display Options:" + self.RESET)
        print(self.CYAN + "   2. Display All Links Scraped")
        print("   3. Display Links not Verified due to Connection Errors")
        print("   4. Display Links with Missing Aria Labels")
        print("   5. Display Broken Links")
        print("   6. Display a Summary of Findings")
        print("-" * 63)
        print(self.YELLOW + "Manage Options:")
        print(self.CYAN + "   7. Empty the Links Google Sheet")
        print("   8. Open Google Sheets")
        print("-" * 63)
        print(self.YELLOW + "Source Code:")
        print(self.CYAN + "   9. Open GitHub")
        print("-" * 63)
        print(self.RED + "0. Exit Program" + self.RESET)
        print(self.CYAN + "-" * 63 + self.RESET)

    def get_user_input(self):
        """
        Get the user's menu choice.
        """
        while True:
            try:
                choice = input(
                    self.YELLOW
                    + "Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): "
                    + self.RESET
                )
                # Convert input to integer
                choice = int(choice)
                if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
                    return choice
                else:
                    print(
                        self.RED
                        + "Invalid choice."
                        + " Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9 or 0.\n"
                        + self.RESET
                    )
            except ValueError:
                print(
                    self.RED
                    + "Invalid input. Please enter a number."
                    + self.RESET
                )

    def get_base_url(self, url):
        """
        Extract the base URL from the given URL.
        """
        parsed_url = urllib.parse.urlparse(url)
        # No path (like in "https://example.com/")
        if not parsed_url.path:
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        else:
            base_url = (
                f"{parsed_url.scheme}://{parsed_url.netloc}"
                f"{parsed_url.path.rstrip('/')}/"
            )
        return base_url

    def write_to_google_sheets(self, data):
        """
        Write data to Google Sheets.
        """
        try:
            # Define the header row
            header = [
                "Link URL",
                "Type",
                "Status",
                "Response",
                "Missing Aria",
            ]

            # Clear existing data (including header)
            self.WORKSHEET.clear()

            # Write the header row to the worksheet
            self.WORKSHEET.append_row(header)

            # Append new data with status, response, and missing aria
            with tqdm(
                total=len(data),
                desc=self.CYAN + "Saving data to Google Sheets",
                unit="row" + self.RESET,
            ) as pbar:
                for link, link_info in data.items():
                    link_type, status, response, missing_aria = (
                        link_info  # Unpack all four values
                    )

                    # Add data row to the worksheet
                    self.WORKSHEET.append_row(
                        [
                            link,
                            link_type,
                            status,
                            response if response is not None else "",
                            missing_aria,
                        ]
                    )
                    pbar.update(1)

            print(
                self.GREEN
                + "Data saved to Google Sheets successfully."
                + self.RESET
            )
        except Exception as e:
            print(
                self.RED + "An unexpected error occurred:",
                str(e) + self.RESET,
            )

    def is_internal_link(self, link, base_url):
        """
        Check if a link is internal based on the base URL.
        """
        parsed_link = urllib.parse.urlparse(link)
        parsed_base_url = urllib.parse.urlparse(base_url)
        return parsed_link.netloc == parsed_base_url.netloc

    def check_external_links(self, soup, base_url):
        """
        Check external links found in the webpage.
        """
        external_links = []

        # Find all the links on the page
        all_links = soup.find_all("a")

        # Loop through all the links and get the href attribute
        for link in all_links:
            # Get the href attribute of the link
            href = link.get("href")
            # Check if href is not None and is not an empty string
            if href:
                # Create absolute URL using base_url and href
                full_link = urllib.parse.urljoin(base_url, href)
                # Check if the full link is an external link
                if not self.is_internal_link(base_url, full_link):
                    # This is an external link
                    external_links.append(full_link)
        return external_links

    def scrape_and_validate_links(self):
        """
        Scrape and validate links from a webpage.
        """
        url = self.get_url_input()
        print(self.CYAN + "You entered: " + url + self.RESET)

        # Clear the Google Sheet first
        self.empty_links_google_sheet()

        # Print the current page being scraped
        print(f"\nScraping {url}...")

        # Extract base URL
        base_url = self.get_base_url(url)

        try:
            response = requests.get(url)
            # Raise an HTTPError if status code is not 200
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(
                self.RED
                + f"An error occurred while fetching the webpage: {e}"
                + self.RESET
            )
            return

        data = {}  # Dictionary to store link data
        links_with_aria = []  # List to store links with aria labels
        links_without_aria = []  # List to store links without aria labels
        if soup:
            # Check all links for aria labels
            for link in soup.find_all("a"):
                href = link.get("href")
                # Join base URL with relative URL to get full URL
                full_link = urljoin(base_url, href)
                if link.get("aria-label"):
                    links_with_aria.append(full_link)
                else:
                    links_without_aria.append(full_link)

            # Update data with missing aria labels for links with aria
            for link in links_with_aria:
                # Determine missing aria
                missing_aria = "yes" if link in links_without_aria else "no"
                # Get status code and response from check_link_status function
                status, response = self.check_link_status(link)
                data[str(link)] = ("internal", status, response, missing_aria)

            # Update data with missing aria labels for links without aria
            for link in links_without_aria:
                # Determine missing aria
                missing_aria = "yes" if link in links_without_aria else "no"
                # Get status code and response from check_link_status function
                status, response = self.check_link_status(link)
                data[str(link)] = ("internal", status, response, missing_aria)

            # Check external links
            external_links = self.check_external_links(soup, base_url)

            # Determine if links are internal or external
            # and check for broken links
            for link in external_links:
                if self.is_internal_link(link, base_url):
                    link_type = "internal"
                else:
                    link_type = "external"
                # Determine missing aria
                missing_aria = "yes" if link in links_without_aria else "no"
                status = self.check_link_status(link)
                data[str(link)] = (
                    link_type,
                    status[0],
                    status[1],
                    missing_aria,
                )

            # Write data to Google Sheets
            try:
                self.write_to_google_sheets(data)
            except Exception as e:
                print(
                    self.RED
                    + "An error occurred while writing data to Google Sheets:",
                    str(e) + self.RESET,
                )

            print(self.GREEN + "Scraping complete!\n" + self.RESET)
            print(self.CYAN + "Total links found:", len(data))
            print("Links with aria labels:", len(links_with_aria))
            print("Links without aria labels:", len(links_without_aria))
            print("External links found:", len(external_links))
            print("Internal links found:", len(data) - len(external_links))
            print(
                "Broken links found:",
                sum(1 for value in data.values() if value[1] == "broken"),
            )

            # Count the number of connection errors
            num_connection_errors = sum(
                1
                for value in data.values()
                if "No connection adapters were found" in str(value[2])
            )
            print("Links with connection errors:", num_connection_errors)

            print(
                self.GREEN
                + "\nPlease check the Google Sheets for more details."
                + self.RESET
            )
            print(
                self.RED
                + "Note: The Google Sheets will be emptied"
                + " when you scrape a new webpage."
                + self.RESET
            )

    def check_link_status(self, link):
        """
        Check the status of a link.
        """
        try:
            response = requests.head(link)
            status_code = response.status_code
            if status_code >= 400:
                # Broken link (404 Not Found)
                return ("broken", f"{status_code} {response.reason}")
            else:
                # Valid link (status code < 400)
                return ("valid", f"{status_code} {response.reason}")
        except requests.exceptions.RequestException as e:
            return ("broken", str(e))  # Broken link due to connection error

    def display_all_links(self):
        """
        Display all links scraped from the last webpage.
        """
        print(
            self.CYAN
            + "Displaying all links scraped from the last webpage...\n"
            + self.RESET
        )
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()

            # Check if there is any data in the worksheet
            if not data or len(data) <= 1:
                print(self.ERROR_MESSAGE)
                return

            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Display DataFrame
            print(df)

        except Exception:
            print(self.ERROR_MESSAGE)

    def get_url_input(self):
        """
        Get the URL input from the user and validate it.
        """
        while True:
            try:
                print(
                    self.GREEN
                    + "You can use the following URL for testing:"
                    + self.RESET
                )
                print(self.YELLOW + "\nexample.com" + self.RESET)
                print(
                    self.YELLOW
                    + "\nhttps://jeffdruid.github.io/link-test/"
                    + self.RESET
                )
                print(
                    self.YELLOW
                    + "\nhttps://www.w3.org/WAI/demos/bad/before/home.html"
                    + self.RESET
                )
                url = input(
                    self.CYAN
                    + "\nEnter the URL you want to scrape: \n"
                    + self.RESET
                )
                # Check if the URL starts with "http://" or "https://"
                if not url.startswith(("http://", "https://")):
                    # If not, add "http://" to the beginning of the URL
                    url = "https://" + url
                if self.validate_url(url):
                    return url
                else:
                    print(
                        self.RED
                        + "Invalid URL. Please try again."
                        + self.RESET
                    )
            except KeyboardInterrupt:
                print(self.RED + "\nProgram terminated by user." + self.RESET)
                exit()

    def validate_url(self, url):
        """
        Validate the URL by sending a HEAD request
        and checking the status code.
        """
        # Send a HEAD request to the URL and check the status code
        try:
            response = requests.head(
                url, allow_redirects=True, stream=True, timeout=5
            )
            print(
                self.GREEN
                + "\nStatus code: "
                + str(response.status_code)
                + self.RESET
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(Back.RED + f"Error: {e}" + self.RESET)
            return False
        except ValueError as e:
            print(f"Invalid URL: {e}")
            return False

    def open_google_sheet(self):
        """
        Open the Google Sheet in a web browser.
        """
        try:
            sheet_url = self.SHEET.url
            os.system(f"start {sheet_url}")
            print(self.CYAN + "\nLink to Google Sheet: " + sheet_url)
        except Exception as e:
            print(self.RED + "\nFailed to open Google Sheet:", e + self.RESET)

    def display_missing_aria(self, missing_aria):
        """
        Display links with missing aria labels.
        """
        try:
            if missing_aria:
                print(
                    "\n"
                    + self.RED
                    + "Links with missing aria labels:"
                    + self.RESET
                )
                for link in missing_aria:
                    print(link)
            else:
                print(
                    "\n"
                    + self.GREEN
                    + "No links with missing aria labels found."
                    + self.RESET
                )
        except Exception as e:
            print(
                "An error occurred while retrieving data from Google Sheets:",
                str(e),
            )

    def display_missing_aria_links_from_sheet(self):
        """
        Display links missing aria labels from the Google Sheets.
        """
        try:
            # Retrieve data from the Google Sheets
            data = self.WORKSHEET.get_all_values()

            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                missing_aria_links = list(
                    df[df["Missing Aria"] == "yes"]["Link URL"]
                )
                self.display_missing_aria(missing_aria_links)
            else:
                print("No data found in Google Sheets.")
        except Exception:
            print(self.ERROR_MESSAGE)

    def print_links_with_connection_errors(self):
        """
        Print links with connection errors from Google Sheets.
        """
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()
        except Exception as e:
            print(
                self.RED
                + "An error occurred while reading data from Google Sheets:",
                str(e) + self.RESET,
            )
            return

        if data:
            # Convert data to a DataFrame for easier manipulation
            df = pd.DataFrame(data[1:], columns=data[0])

            # Count the number of connection errors
            if "Response" in df.columns:
                num_connection_errors = len(
                    df[
                        df["Response"].str.contains(
                            "No connection adapters were found"
                        )
                    ]
                )

                if num_connection_errors > 0:
                    print(
                        self.RED
                        + "Links not verified due to connection errors:"
                        + self.RESET
                    )
                    # Filter and print links with connection errors
                    connection_errors = df[
                        df["Response"].str.contains(
                            "No connection adapters were found"
                        )
                    ]
                    for index, row in connection_errors.iterrows():
                        print(row["Link URL"])
                else:
                    print(
                        self.GREEN + "No links with connection errors found."
                    )
            else:
                print(self.ERROR_MESSAGE)
        else:
            print(self.ERROR_MESSAGE)

    def display_broken_links(self):
        """
        Display broken links from the last webpage.
        """
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()

            # Check if there is any data in the worksheet
            if not data:
                print("No links found.")
                return

            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Filter DataFrame to get broken links
            broken_links = df[df["Status"] == "broken"]

            if broken_links.empty:
                print(self.GREEN + "No broken links found." + self.RESET)
            else:
                print(self.RED + "Broken links found:" + self.RESET)
                for broken_link in broken_links["Link URL"]:
                    print(broken_link)

        except Exception:
            print(self.ERROR_MESSAGE)

    def open_github(self):
        """
        Open the GitHub link in a web browser.
        """
        github_link = "https://github.com/jeffdruid/link-validator"
        print("\n" + self.GREEN + "GitHub link: " + github_link + self.RESET)
        try:
            webbrowser.open(github_link)
        except Exception as e:
            print(self.RED + "\nFailed to open GitHub:", e + self.RESET)

    def empty_links_google_sheet(self):
        """
        Empty the links Google Sheet.
        """
        try:
            # Clear existing data (including header)
            self.WORKSHEET.clear()
        except Exception as e:
            print(
                self.RED + "An unexpected error occurred:",
                str(e) + self.RESET,
            )

    def summarize_findings(
        self,
        num_links_scraped,
        num_links_with_aria,
        num_internal_links,
        num_external_links,
        num_missing_aria,
        num_broken_links,
        num_connection_errors,
    ):
        """
        Generate a summary of findings and present them with ASCII art.
        """
        print("\n" + self.CYAN + "Summary of Findings:" + self.RESET)
        print("+" + "-" * 40 + "+")
        print(
            "| {:<20} {:<15} |".format(
                self.YELLOW + "Metric", "Count" + self.RESET
            )
        )
        print("+" + "-" * 40 + "+")
        print(
            "| {:<20} {:<15} |".format(
                self.GREEN + "Links Scraped",
                str(num_links_scraped) + self.RESET,
            )
        )
        print(
            "| {:<20} {:<15} |".format(
                self.GREEN + "Internal Links",
                str(num_internal_links) + self.RESET,
            )
        )
        print(
            "| {:<20} {:<15} |".format(
                self.GREEN + "External Links",
                str(num_external_links) + self.RESET,
            )
        )
        print(
            "| {:<20} {:<15} |".format(
                self.GREEN + "Links with Aria",
                str(num_links_with_aria) + self.RESET,
            )
        )
        (
            print(
                "| {:<20} {:<15} |".format(
                    self.RED + "Missing Aria",
                    str(num_missing_aria) + self.RESET,
                )
            )
            if num_missing_aria > 0
            else print(
                "| {:<20} {:<15} |".format(
                    "Missing Aria Labels", num_missing_aria
                )
            )
        )
        (
            print(
                "| {:<20} {:<15} |".format(
                    self.RED + "Broken Links",
                    str(num_broken_links) + self.RESET,
                )
            )
            if num_broken_links > 0
            else print(
                "| {:<20} {:<15} |".format(
                    self.GREEN + "Broken Links",
                    str(num_broken_links) + self.RESET,
                )
            )
        )
        (
            print(
                "| {:<20} {:<15} |".format(
                    self.RED + "Not Verified",
                    str(num_connection_errors) + self.RESET,
                )
            )
            if num_connection_errors > 0
            else print(
                "| {:<20} {:<15} |".format(
                    self.GREEN + "Errors",
                    str(num_connection_errors) + self.RESET,
                )
            )
        )
        print("+" + "-" * 40 + "+")

    def display_summary_of_findings(self):
        """
        Display a summary of findings.
        """
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()

            # Check if there is any data in the worksheet
            if not data:
                print("No links found in Google Sheets.")
                return

            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Check if 'Status' column exists
            if "Status" not in df.columns:
                print(self.ERROR_MESSAGE)
                return

            # Count the number of links scraped
            num_links_scraped = len(df)

            # Count the number of aria labels found if the column exists
            if "Missing Aria" in df.columns:
                num_links_with_aria = len(df[df["Missing Aria"] == "no"])
            else:
                num_links_with_aria = 0

            # Count the number of internal links found if the column exists
            if "Type" in df.columns:
                num_internal_links = len(df[df["Type"] == "internal"])
            else:
                num_internal_links = 0

            # Count the number of external links found if the column exists
            if "Type" in df.columns:
                num_external_links = len(df[df["Type"] == "external"])
            else:
                num_external_links = 0

            # Count the number of missing aria labels if the column exists
            if "Missing Aria" in df.columns:
                num_missing_aria = len(df[df["Missing Aria"] == "yes"])
            else:
                num_missing_aria = 0

            # Count the number of connection errors
            if "Response" in df.columns:
                num_connection_errors = len(
                    df[
                        df["Response"].str.contains(
                            "No connection adapters were found"
                        )
                    ]
                )
            else:
                num_connection_errors = 0

            # Count the number of broken links if the column exists
            if "Status" in df.columns:
                num_broken_links = len(df[df["Status"] == "broken"])
            else:
                num_broken_links = 0

            # Display the summary
            self.summarize_findings(
                num_links_scraped,
                num_links_with_aria,
                num_internal_links,
                num_external_links,
                num_missing_aria,
                num_broken_links,
                num_connection_errors,
            )

        except Exception as e:
            print("An unexpected error occurred:", str(e))

    def ask_continue(self):
        """
        Ask the user if they want to continue.
        """
        while True:
            choice = input(
                self.YELLOW + "\nDo you want to continue? (y/n): " + self.RESET
            )
            if choice.lower() in ["y", "yes"]:
                # Clear the console
                self.clear_console()

                self.main()  # Continue with the main program loop
            elif choice.lower() in ["n", "no"]:
                print(self.RED + "\nExiting the program..." + self.RESET)
                exit()
            else:
                print(
                    self.RED
                    + "Invalid choice. Please enter 'y' or 'n'."
                    + self.RESET
                )

    def clear_console(self):
        """
        Clear the console.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def main(self):
        """
        The main function of the Link-Validator Tool.
        """
        self.print_welcome_message()
        try:
            while True:
                self.print_instructions()

                choice = self.get_user_input()

                self.clear_console()

                if choice == 1:
                    self.scrape_and_validate_links()
                elif choice == 2:
                    self.display_all_links()
                elif choice == 3:
                    self.print_links_with_connection_errors()
                elif choice == 4:
                    self.display_missing_aria_links_from_sheet()
                elif choice == 5:
                    self.display_broken_links()
                elif choice == 6:
                    self.display_summary_of_findings()
                elif choice == 7:
                    self.empty_links_google_sheet()
                    print(
                        "\n"
                        + self.GREEN
                        + "The Google Sheet has been emptied."
                        + self.RESET
                    )
                elif choice == 8:
                    self.open_google_sheet()
                elif choice == 9:
                    self.open_github()
                elif choice == 0:
                    print(self.RED + "\nExiting the program..." + self.RESET)
                    exit()
                self.ask_continue()
        # Handle keyboard interrupt
        except KeyboardInterrupt:
            print(self.RED + "\nProgram terminated by user." + self.RESET)
            exit()


if __name__ == "__main__":
    link_validator = LinkValidator()
    link_validator.main()
