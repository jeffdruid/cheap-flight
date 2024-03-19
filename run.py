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
from urllib.parse import urljoin

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
        
        print(self.MAGENTA + "Menu options:" + self.RESET)
        print(self.CYAN + "-" * 63)
        print("1. Scrape and Validate Links from a Webpage")
        print("-" * 63)
        print(" Display Options:\n")
        print("   2. Display All Links Scraped from the Last Webpage")
        print("   3. Display Invalid Links Scraped from the Last Webpage")
        print("   4. Display Links with Missing Aria Labels from the Last Webpage")
        print("   5. Display Broken Links from the Last Webpage")
        print("   6. Display a Summary of Findings from the Last Webpage")
        print("-" * 63)
        print(" Manage Options:\n")
        print("   7. Empty the Links Google Sheet")
        print("   8. Open Google Sheets")
        print("-" * 63)
        print(" Additional Information:\n")
        print("   9. Open GitHub")
        print("-" * 63)
        print("0. Exit Program")
        print("-" * 63 + self.RESET)

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
        if not parsed_url.path:  # No path (like in "https://example.com/")
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        else:
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rstrip('/')}/"
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
            header = ['Link URL', 'Type', 'Status', 'Response', 'Missing Aria']

            # Clear existing data (including header)
            self.WORKSHEET.clear()

            # Write the header row to the worksheet
            self.WORKSHEET.append_row(header)

            # Append new data with status, response, and missing aria
            with tqdm(total=len(data), desc=self.CYAN + "Saving data to Google Sheets", unit="row" + self.RESET) as pbar:
                for link, link_info in data.items():
                    link_type, status, response, missing_aria = link_info  # Unpack all four values

                    # Add data row to the worksheet
                    self.WORKSHEET.append_row([link, link_type, status, response if response is not None else '', missing_aria])
                    pbar.update(1)

            print(self.GREEN + "Data saved to Google Sheets successfully." + self.RESET)
        except Exception as e:
            print(self.RED + "An unexpected error occurred:", str(e) + self.RESET)
            
    def is_internal_link(self, base_url, link):
        """
        Check if a link is internal based on the base URL.
        """
        parsed_link = urllib.parse.urlparse(link)
        parsed_base_url = urllib.parse.urlparse(base_url)
        
        # Check if the link has the same scheme and netloc (domain) as the base URL
        is_internal = parsed_link.scheme == parsed_base_url.scheme and parsed_link.netloc == parsed_base_url.netloc
        
        return is_internal

    def check_internal_links(self, soup, base_url):
        """
        Check internal links found in the webpage.
        """
        internal_links = set()  # Set to store internal links

        # Find all the links on the page
        all_links = soup.find_all("a")

        # Loop through all the links and get the href attribute
        for link in all_links:
            # Get the href attribute of the link
            href = link.get("href")
            # Check if href is not None and is not an empty string
            if href is not None and href.strip() != "":
                # Create absolute URL using base_url and href
                full_link = urllib.parse.urljoin(base_url, href)
                # Check if the full_link is internal or pointing to the same page with "#"
                if self.is_internal_link(base_url, full_link) or href == "#":
                    internal_links.add(full_link)

        return internal_links

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

        data = {}  # Dictionary to store link data
        links_with_aria = []  # List to store links with aria labels
        links_without_aria = []    # List to store links without aria labels
        if soup:
            # Check all links for aria labels
            for link in soup.find_all("a"):
                href = link.get('href')
                full_link = urljoin(url, href)  # Join base URL with relative URL to get full URL
                if link.get('aria-label'):
                    links_with_aria.append(full_link)
                else:
                    links_without_aria.append(full_link)
            
            # Update data with missing aria labels for links with aria
            for link in links_with_aria:
                # Check if the link is already in data
                if str(link) in data:
                    # Get the existing values for the link
                    link_type, status, response = data[str(link)][:3]
                    # Update the missing aria column to 'no'
                    data[str(link)] = (link_type, status, response, 'no')

            # Update data with missing aria labels for links without aria
            for link in links_without_aria:
                # Check if the link is already in data
                if str(link) in data:
                    # Get the existing values for the link
                    link_type, status, response = data[str(link)][:3]
                    # Update the missing aria column to 'yes'
                    data[str(link)] = (link_type, status, response, 'yes')

            # Extract base URL
            base_url = self.get_base_url(url)

            # Check internal links
            internal_links = self.check_internal_links(soup, base_url)

            # Check external links
            external_links = self.check_external_links(soup, base_url)

            # Convert internal_links to a list before concatenating
            all_links = list(internal_links) + external_links
            # REMOVE 
            # Check for missing aria labels while scraping
            # missing_aria = self.check_missing_aria(soup.find_all("a"))

            # Update data with missing aria labels
            # for link in missing_aria:
            #     if str(link) in data:
            #         data[str(link)] = (data[str(link)][0], data[str(link)][1], data[str(link)][2], 'yes')
            #     else:
            #         # Add missing aria link to data
            #         data[str(link)] = ('internal' if link in internal_links else 'external', 'missing_aria', 'None', 'yes')

            # Check for broken links and update data
            link_status = self.check_broken_links(all_links)
            for link, status in link_status.items():
                if link in internal_links:
                    link_type = 'internal'
                    # Check missing aria for internal links
                    missing_aria = 'yes' if link in links_without_aria else 'no'
                    print(f"Missing aria for internal link {link}: {missing_aria}")
                else:
                    link_type = 'external'
                    # For external links, keep the existing missing aria value
                    missing_aria = 'yes' if link in links_without_aria else 'no2' if status[0] == 'broken' else 'no'
                    print(f"Missing aria for external link {link}: {missing_aria}")
                data[str(link)] = (link_type, status[0], status[1], missing_aria)  # Set response to the actual response code for broken links
            print(f"Links without aria: {links_without_aria}")
            print(f"Links with aria: {links_with_aria}")
            print(f"Internal links {internal_links}")
            print(f"External links {external_links}")

            # Write data to Google Sheets
            try:
                self.write_to_google_sheets(data)
            except Exception as e:
                print(self.RED + "An error occurred while writing data to Google Sheets:", str(e) + self.RESET)

            print("Scraping complete!\n")
            print("Links with aria labels:", len(links_with_aria))
            print("Links without aria labels:", len(links_without_aria))
    
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
                print(self.CYAN + "\nhttps://jeffdruid.github.io/link-test/" + self.RESET)
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

    def check_missing_aria(self, all_links):
        """
        Check for missing aria labels in anchor elements.
        """
        try:
            # Initialize a dictionary to store missing aria labels for each link
            missing_aria_dict = {}

            # Loop through all links
            for link in all_links:
                # Check for anchor elements
                if link.name == 'a':
                    # Check if aria-label attribute exists and is not empty
                    aria_label = link.get('aria-label')
                    # REMOVE
                    # if not aria_label or aria_label.strip() == '':
                    #     missing_aria_dict[str(link)] = 'yes'  # Missing aria label
                    # else:
                    #     missing_aria_dict[str(link)] = 'no'   # Aria label exists

            print("\n" + self.GREEN + "Missing aria labels checked successfully." + self.RESET)
            print("Number of links checked:", len(all_links))
            print("Number of links with missing aria labels:", sum(1 for value in missing_aria_dict.values() if value == 'yes'))
            print("Number of links with aria labels:", sum(1 for value in missing_aria_dict.values() if value == 'no'))
            return missing_aria_dict
        except Exception as e:
            print("Error:", e)
            return {}

    def display_missing_aria(self, missing_aria):
        """
        Display links with missing aria labels.
        """
        if missing_aria:
            print("\n" + self.RED + "Links with missing aria labels:" + self.RESET)
            for link in missing_aria:
                print(link)
        else:
            print("\n" + self.GREEN + "No links with missing aria labels found." + self.RESET)

    def display_missing_aria_links_from_sheet(self):
        """
        Display links missing aria labels from the Google Sheets.
        """
        try:
            # Retrieve data from the Google Sheets
            data = self.WORKSHEET.get_all_values()
            
            if data:
                df = pd.DataFrame(data[1:], columns=data[0])
                missing_aria_links = list(df[df['Missing Aria'] == 'yes']['Link URL'])
                self.display_missing_aria(missing_aria_links)
            else:
                print("No data found in Google Sheets.")
        except Exception as e:
            print("An error occurred while retrieving data from Google Sheets:", str(e))

    def check_broken_links(self, links):
        """
        Check for broken links in the provided list of links.
        Returns a dictionary mapping each link to its status (valid, broken, error, etc.)
        and its response code.
        """
        print(self.CYAN + "Checking for broken links..." + self.RESET)
        link_status = {}

        # Initialize the progress bar
        pbar = tqdm(total=len(links), desc=self.CYAN + "Checking links", unit="link" + self.RESET)

        # Loop through all the links and check for broken links
        for link in links:
            try:
                # Skip JavaScript void links
                if link.startswith("javascript:"):
                    print(f"Skipping JavaScript void link: {link}")
                    link_status[link] = ('skipped', None)
                    continue

                # Handle URLs with unsupported schemes
                if not link.startswith(("http://", "https://")):
                    print(f"Unsupported URL scheme for link: {link}")
                    link_status[link] = ('unsupported_scheme', 'None')
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
                print(f"Error checking link {link}")
                link_status[link] = ('error', '-')
                # Check if the hostname resolution failed
                if isinstance(e, requests.exceptions.ConnectionError):
                    print(f"Hostname resolution failed for link: {link}")
                    link_status[link] = ('broken', 'hostname_resolution_failed')
            except Exception as e:
                # Handle other exceptions
                error_msg = str(e).split('\n')[0]  # Extract the first line of the error message
                print(f"An unexpected error: {error_msg}")
                link_status[link] = ('unexpected_error', '-')

            pbar.update(1)  # Update the progress bar

        pbar.close()  # Close the progress bar
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

    def display_invalid_links(self):
        """
        Display invalid links with unsupported schemes scraped from the last webpage.
        """
        print(self.CYAN + "Displaying invalid links scraped from the last webpage...\n" + self.RESET)
        try:
            # Fetch all data from the worksheet
            data = self.WORKSHEET.get_all_values()

            # Check if there is any data in the worksheet
            if not data:
                print("No links found.")
                return
            
            # Convert data to DataFrame
            df = pd.DataFrame(data[1:], columns=data[0])

            # Filter DataFrame to get invalid links with unsupported schemes
            invalid_links = df[(df['Status'] == 'unsupported_scheme')]

            if invalid_links.empty:
                print(self.GREEN + "No invalid links found." + self.RESET)
            else:
                print(self.RED + "Invalid links found:" + self.RESET)
                for invalid_link in invalid_links['Link URL']:
                    print(invalid_link)
        
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
            
    def summarize_findings(self, num_links_scraped, num_missing_aria, num_broken_links):
        """
        Generate a summary of findings and present them with ASCII art.
        """
        print("\n" + self.GREEN + "Summary of Findings:" + self.RESET)
        print("+" + "-" * 40 + "+")
        print("| {:<20} {:<15} |".format("Metric", "Count"))
        print("+" + "-" * 40 + "+")
        print("| {:<20} {:<15} |".format("Links Scraped", num_links_scraped))
        print("| {:<20} {:<15} |".format("Missing Aria Labels", num_missing_aria))
        print("| {:<20} {:<15} |".format("Broken Links", num_broken_links))
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
            if 'Status' not in df.columns:
                print(self.RED + "No links have been scraped yet." + self.RESET)
                return

            # Count the number of links scraped
            num_links_scraped = len(df)

            # Count the number of missing aria labels if the column exists
            if 'Missing Aria' in df.columns:
                num_missing_aria = len(df[df['Missing Aria'] == 'yes'])
            else:
                num_missing_aria = 0

            # Count the number of broken links if the column exists
            if 'Status' in df.columns:
                num_broken_links = len(df[df['Status'] == 'broken'])
            else:
                num_broken_links = 0

            # Display the summary
            self.summarize_findings(num_links_scraped, num_missing_aria, num_broken_links)
        
        except Exception as e:
            print("An unexpected error occurred:", str(e))
    
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
                    self.display_invalid_links()
                elif choice == 4:
                    self.display_missing_aria_links_from_sheet()
                elif choice == 5:
                    self.display_broken_links()
                elif choice == 6:
                    self.display_summary_of_findings()
                elif choice == 7:
                    self.empty_links_google_sheet()
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
