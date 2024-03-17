import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Back, Fore, Style
import os
import urllib.parse
import gspread
from google.oauth2.service_account import Credentials
import webbrowser

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
        self.ERROR_MESSAGE = (self.RED + "\nNo links found. Please scrape a webpage first." + self.RESET)
        self.initialize_colorama()
        
        self.SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]

        # Google Sheets API credentials
        self.CREDS = Credentials.from_service_account_file('creds.json')
        self.SCOPED_CREDS = self.CREDS.with_scopes(self.SCOPE)
        self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
        self.SHEET = self.GSPREAD_CLIENT.open('LinkValidator')
        self.WORKSHEET = self.SHEET.sheet1
                
    def initialize_colorama(self):
        """
        Initialize colorama and set the color for the welcome message.
        """
        colorama.init()

    def print_welcome_message(self):
        """
        Print the welcome message for the Link-Validator Tool.
        """
        print(Style.BRIGHT + Back.GREEN + Fore.WHITE + "\nWelcome to the Link-Validator Tool!\n" + self.RESET + self.YELLOW + "\nThis tool allows you to scrape a webpage and validate all the links." + self.RESET)

    def print_instructions(self):
        """
        Display the instructions for using the Link-Validator Tool.
        """    
        print(self.MAGENTA + "\nPlease select an option from the menu below:")
        print(self.CYAN + "1. Scrape and validate links from a webpage")
        print("2. Display all links scraped from the last webpage")
        print("3. Display links with missing alt tags")
        print("4. Display links with missing aria labels")
        print("5. Empty the links Google Sheet")
        print("6. Open Google Sheets")
        print("7. Display a summary of findings")
        print("8. Display broken links from the last webpage")
        print("9. Open GitHub")
        print("0. Exit" + self.RESET)
        print("")

    def get_user_input(self):
        """
        Get the user's menu choice.
        """
        while True:
            try:
                choice = input(self.YELLOW + "Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): " + self.RESET)
                # Convert input to integer
                choice = int(choice)
                if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
                    return choice
                else:
                    print(self.RED + "Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9 or 0.\n" + self.RESET)
            except ValueError:
                print(self.RED + "Invalid input. Please enter a number." + self.RESET)

    def get_base_url(self, url):
        """
        Extract the base URL from the given URL.
        """
        parsed_url = urllib.parse.urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{os.path.dirname(parsed_url.path)}"
        return base_url
    
    def test_google_sheets(self):
        """
        Test writing data to Google Sheets.
        """
        test_data = [['Test1', 'Test2', 'Test3'], ['Value1', 'Value2', 'Value3']]
        self.write_to_google_sheets(test_data)
    
    def write_to_google_sheets(self, data):
        """
        Write data to Google Sheets.
        """
        try:
            # Define the header row
            header = ['Link URL', 'Type', 'Status', 'Response']

            # Clear existing data (including header)
            self.WORKSHEET.clear()

            # Write the header row to the worksheet
            self.WORKSHEET.append_row(header)

            # Append new data with status
            with tqdm(total=len(data), desc= self.CYAN + "Saving data to Google Sheets", unit="row" + self.RESET) as pbar:
                for link, (status, response) in data.items():
                    self.WORKSHEET.append_row([link, '', status, response])
                    pbar.update(1)

            print(self.GREEN + "Data saved to Google Sheets successfully." + self.RESET)
        except Exception as e:
            print(self.RED + "An unexpected error occurred:", str(e) + self.RESET)
            
    def scrape_and_validate_links(self):
        """
        Scrape and validate links from a webpage.
        """
        url = self.get_url_input()
        print("You entered: " + url)

        # Clear the Google Sheet first
        self.empty_links_google_sheet()

        # Print the current page being scraped
        print(f"\nScraping {url}...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError if status code is not 200
            soup = BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(self.RED + f"An error occurred while fetching the webpage: {e}" + self.RESET)
            return

        data = []  # List to store URLs

        # Load the existing data from Google Sheets
        try:
            data = self.WORKSHEET.get_all_values()
            if not data:
                print("No links found in Google Sheets.")
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return

        if soup:
            # Find all the links on the page
            all_links = soup.find_all("a")

            # Extract base URL
            base_url = self.get_base_url(url)

            # Loop through all the links and get the href attribute
            for link in all_links:
                # Get the href attribute of the link
                href = link.get("href")
                # Check if href is not None and is not an empty string
                if href:
                    # Check if href is a relative path
                    if not urllib.parse.urlparse(href).netloc:
                        # Create absolute URL using base_url and href
                        full_link = urllib.parse.urljoin(base_url, href)
                    else:
                        # Use href directly as it's already an absolute URL
                        full_link = href
                    # Add full link to data if it's not empty
                    if full_link:
                        data.append([full_link])

            # Print the number of links found on the page
            num_links_scraped = len(data)
            print(self.GREEN + f"Found {num_links_scraped} links on {url}." + self.RESET)

            # Check for missing alt tags and capture the returned list
            missing_alt = self.check_missing_alt(all_links)
            num_missing_alt = len(missing_alt)

            # Check for missing aria labels and capture the returned list
            missing_aria = self.check_missing_aria(all_links)
            num_missing_aria = len(missing_aria)

            # Filter out empty lists from data
            data = [link[0] for link in data if link]

            # Check for broken links
            link_status = self.check_broken_links(data)
           
            # Count the number of broken links
            num_broken_links = sum(1 for status in link_status.values() if status[0] == 'broken')

            # Write data to Google Sheets
            try:
                self.write_to_google_sheets(link_status)  # Write extracted links to Google Sheets
            except Exception as e:
                print(self.RED + "An error occurred while writing data to Google Sheets:", str(e) + self.RESET)

            # Sort the data by type
            self.sort_data_by_type()

            print("Scraping complete!\n")
    
    def display_all_links(self):
        """
        Display all links scraped from the last webpage.
        """
        print(self.CYAN + "Displaying all links scraped from the last webpage...\n" + self.RESET)
        # Check if the worksheet exists
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()

            # Check if there is any data in the worksheet
            if not data:
                print("No links found.")
                return
            
            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])
            
            # Display DataFrame
            print(df)
        
        except Exception as e:
            print(self.ERROR_MESSAGE)

    def get_url_input(self):
        """
        Get the URL input from the user and validate it.
        """
        while True:
            try:
                url = input(self.CYAN + "\nEnter the URL you want to scrape: \n" + self.RESET)
                # Check if the URL starts with "http://" or "https://"
                if not url.startswith(("http://", "https://")):
                    # If not, add "http://" to the beginning of the URL
                    url = "https://" + url
                if self.validate_url(url):
                    return url
                else:
                    print(self.RED + "Invalid URL. Please try again." + self.RESET)
            except KeyboardInterrupt:
                print(self.RED + "\nProgram terminated by user." + self.RESET)
                exit()

    def validate_url(self, url):
        """
        Validate the URL by sending a HEAD request and checking the status code.
        """
        # Send a HEAD request to the URL and check the status code
        try:
            response = requests.head(url, allow_redirects=True, stream=True, timeout=5)
            print(self.GREEN + "Status code: " + str(response.status_code) + self.RESET)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(Back.RED + f"Error: {e}" + self.RESET)
            return False
        except ValueError as e:
            print(f"Invalid URL: {e}")
            return False

    def sort_data_by_type(self):
        """
        Sort the data by type and update the 'Type' column in the Google Sheets.
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

            # Add a new column 'Type'
            df['Type'] = df['Link URL'].apply(self.get_link_type)

            # Sort DataFrame by 'Type' with progress bar
            sorted_df = df.sort_values(by="Type")
            total_rows = len(sorted_df)
            with tqdm(total=total_rows, desc=self.CYAN + "Sorting data", unit="row" + self.RESET) as pbar:
                for index, row in sorted_df.iterrows():
                    self.WORKSHEET.update([row.values.tolist()], f'A{index+2}')
                    pbar.update(1)

            print(self.GREEN + "Data sorted by type successfully." + self.RESET)
        except Exception as e:
            print(self.ERROR_MESSAGE)

    def get_link_type(self, link):
        """
        Get the type of the link.
        """
        # Check if the link is external or internal
        if link.startswith("http://") or link.startswith("https://"):
            return "external"
        else:
            return "internal"
        
    def open_google_sheet(self):
        """
        Open the Google Sheet in a web browser.
        """
        try:
            sheet_url = self.SHEET.url
            os.system(f"start {sheet_url}")
            print("\n" + self.GREEN + "Google Sheet has been opened in a web browser." + self.RESET)
        except Exception as e:
            print(self.RED + "\nFailed to open Google Sheet:", e + self.RESET)

    def check_missing_alt(self, all_links):
        """
        Check for missing alt attributes in img elements.
        """
        try:
            # Initialize a list to store links with missing alt tags
            missing_alt = []

            # Loop through all links
            for link in all_links:
                # Check for missing alt tags in img elements
                if link.name == 'img' and (not link.get('alt') or link.get('alt').strip() == ''):
                    missing_alt.append(link)
                    
            print("Number of missing alt tags:", len(missing_alt))
            return missing_alt
        except Exception as e:
            print("Error:", e)
            return []

    def check_missing_aria(self, all_links):
        """
        Check for missing aria labels in anchor elements.
        """
        try:
            # Initialize a list to store links with missing aria labels
            missing_aria = []

            # Loop through all links
            for link in all_links:
                # Check for anchor elements
                if link.name == 'a':
                    # Check if aria-label attribute exists and is not empty
                    aria_label = link.get('aria-label')
                    if not aria_label or aria_label.strip() == '':
                        missing_aria.append(link)

            print("Number of missing aria labels:", len(missing_aria))
            return missing_aria
        except Exception as e:
            print("Error:", e)
            return []

    def display_missing_alt(self, missing_alt):
        """
        Display links with missing alt tags.
        """
        if missing_alt:
            print("\n" + self.GREEN + "Links with missing alt tags:" + self.RESET)
            for link in missing_alt:
                print(link)
        else:
            print("\n" + self.GREEN + "No links with missing alt tags found." + self.RESET)

    def display_missing_aria(self, missing_aria):
        """
        Display links with missing aria labels.
        """
        if missing_aria:
            print("\n" + self.GREEN + "Links with missing aria labels:" + self.RESET)
            for link in missing_aria:
                print(link)
        else:
            print("\n" + self.GREEN + "No links with missing aria labels found." + self.RESET)

    def check_broken_links(self, links):
        """
        Check for broken links in the provided list of links.
        Returns a dictionary mapping each link to its status (valid or broken)
        and its status code.
        """
        print(self.CYAN + "Checking for broken links..." + self.RESET)
        link_status = {}

        # Loop through all the links and check for broken links
        for link in tqdm(links, desc=self.CYAN + "Checking links", unit="link" + self.RESET):
            try:
                # Skip JavaScript void links
                if link.startswith("javascript:"):
                    print(f"Skipping JavaScript void link: {link}")
                    link_status[link] = ('skipped', None)
                    continue

                # Handle URLs with unsupported schemes
                if not link.startswith(("http://", "https://")):
                    print(f"Unsupported URL scheme for link: {link}")
                    link_status[link] = ('unsupported_scheme', None)
                    continue

                # Send a HEAD request to the link and check the status code
                response = requests.head(link, allow_redirects=True, timeout=5)
                if response.status_code >= 400:
                    print(f"Broken link found: {link}")
                    link_status[link] = ('broken', response.status_code)
                else:
                    link_status[link] = ('valid', response.status_code)

            except requests.exceptions.RequestException as e:
                # Handle connection errors
                error_msg = str(e).split('\n')[0]  # Extract the first line of the error message
                print(f"Error checking link {link}: {error_msg}")
                link_status[link] = ('error', None)
                # Check if the hostname resolution failed
                if isinstance(e, requests.exceptions.ConnectionError):
                    print(f"Hostname resolution failed for link: {link}")
                    link_status[link] = ('broken', None)
            except Exception as e:
                # Handle other exceptions
                error_msg = str(e).split('\n')[0]  # Extract the first line of the error message
                print(f"An unexpected error: {error_msg}")
                link_status[link] = ('unexpected_error', None)

        print(self.GREEN + "Broken links checked successfully." + self.RESET)
        print("Number of broken links:", sum(1 for status in link_status.values() if status[0] == 'broken'))
        return link_status

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
            broken_links = df[df['Status'] == 'broken']

            if broken_links.empty:
                print(self.GREEN + "No broken links found." + self.RESET)
            else:
                print(self.RED + "Broken links found:" + self.RESET)
                for broken_link in broken_links['Link URL']:
                    print(broken_link)
        
        except Exception as e:
            print(self.ERROR_MESSAGE)

    def open_github(self):
        """
        Open the GitHub link in a web browser.
        """
        github_link = "https://github.com/jeffdruid/link-validator"
        print("\n" + self.GREEN + "GitHub link: " + github_link + self.RESET)
        try:
            webbrowser.open(github_link)
            print("\n" + self.GREEN + "GitHub has been opened in a new tab." + self.RESET)
        except Exception as e:
            print(self.RED + "\nFailed to open GitHub:", e + self.RESET)

    def empty_links_google_sheet(self):
        """
        Empty the links Google Sheet.
        """
        try:
            # Clear existing data (including header)
            self.WORKSHEET.clear()
            # print("\n" + self.GREEN + "The Google Sheet has been emptied." + self.RESET)
        except Exception as e:
            print(self.RED + "An unexpected error occurred:", str(e) + self.RESET)
            
    def summarize_findings(self, num_links_scraped, num_missing_alt, num_missing_aria, num_broken_links):
        """
        Generate a summary of findings and present them with ASCII art.
        """
        print("\n" + self.GREEN + "Summary of Findings:" + self.RESET)
        print("+" + "-" * 40 + "+")
        print("| {:<20} {:<15} |".format("Metric", "Count"))
        print("+" + "-" * 40 + "+")
        print("| {:<20} {:<15} |".format("Links Scraped", num_links_scraped))
        print("| {:<20} {:<15} |".format("Missing Alt Tags", num_missing_alt))
        print("| {:<20} {:<15} |".format("Missing Aria Labels", num_missing_aria))
        print("| {:<20} {:<15} |".format("Broken Links", num_broken_links))
        print("+" + "-" * 40 + "+")
    
    def display_summary_of_findings(self):
        """
        Display a summary of findings.
        """
        # Load the existing data from Google Sheets
        try:
            data = self.WORKSHEET.get_all_values()
            if not data:
                print("No links found in Google Sheets.")
                return
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return

        # Convert data to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Count the number of links scraped
        num_links_scraped = len(df)

        # Count the number of missing alt tags if the column exists
        if 'Alt Tag' in df.columns:
            num_missing_alt = len(df[df['Type'] == 'image'][df['Alt Tag'].isnull()])
        else:
            num_missing_alt = 0

        # Count the number of missing aria labels if the column exists
        if 'Aria Label' in df.columns:
            num_missing_aria = len(df[df['Type'] == 'anchor'][df['Aria Label'].isnull()])
        else:
            num_missing_aria = 0

        # Count the number of broken links
        num_broken_links = len(df[df['Status'] == 'broken'])

        # Display the summary
        self.summarize_findings(num_links_scraped, num_missing_alt, num_missing_aria, num_broken_links)
    
    def ask_continue(self):
        """
        Ask the user if they want to continue.
        """
        while True:
            choice = input(self.YELLOW + "\nDo you want to continue? (y/n): " + self.RESET)
            if choice.lower() in ["y", "yes"]:
                # Clear the console
                self.clear_console()
                
                self.main()  # Continue with the main program loop
            elif choice.lower() in ["n", "no"]:
                print(self.RED + "\nExiting the program..." + self.RESET)
                exit()
            else:
                print(self.RED + "Invalid choice. Please enter 'y' or 'n'." + self.RESET)

    def clear_console(self):
        """
        Clear the console.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

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
                    self.display_missing_alt(missing_alt=[])
                elif choice == 4:
                    self.display_missing_aria(missing_aria=[])
                elif choice == 5:
                    self.empty_links_google_sheet()
                elif choice == 6:
                    self.open_google_sheet()
                elif choice == 7:
                    self.display_summary_of_findings()
                elif choice == 8:
                    self.display_broken_links()
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
