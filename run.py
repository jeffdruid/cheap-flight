import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Back, Fore, Style
import os
import shutil
import urllib.parse
import gspread
from google.oauth2.service_account import Credentials

class LinkValidator:
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
        print("7. Not implemented yet")
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
                choice = int(input(self.YELLOW + "Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): " + self.RESET))
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
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
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
            # Clear existing data (including header)
            self.WORKSHEET.clear()

            # Define the header row
            header = ['Link URL', 'Type', 'Status']

            # Write the header row to the worksheet
            self.WORKSHEET.update('A1', [header])

            # Ensure each row of data has exactly three columns
            for row in data:
                if len(row) != 3:
                    # If the number of columns is incorrect, adjust the data
                    if len(row) == 1:
                        # If only the link URL is provided, add empty values for 'Type' and 'Status'
                        row.extend(['', ''])
                    else:
                        # If more than three columns are provided, trim the extra columns
                        row = row[:3]

            # Append new data
            self.WORKSHEET.append_rows(data)

            print(self.GREEN + "Data written to Google Sheets successfully." + self.RESET)
        except Exception as e:
            print(self.RED + "An unexpected error occurred:", str(e) + self.RESET)
    
    def scrape_and_validate_links(self):
        """
        Scrape and validate links from a webpage.
        """
        url = self.get_url_input()
        print("You entered: " + url)
        data = []  # List to store data

        # Print the current page being scraped
        print(f"\nScraping {url}...")

        # Load the existing data from Google Sheets
        try:
            data = self.WORKSHEET.get_all_values()
            if not data:
                print("No links found in Google Sheets.")
                df = pd.DataFrame(columns=['Link URL'])  # Initialize DataFrame with only 'Link URL' column
            else:
                # Construct DataFrame with explicit column names
                df = pd.DataFrame(data, columns=['Link URL'])
        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return

        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        if soup:
            # Find all the links on the page
            all_links = soup.find_all("a")

            # Extract base URL
            base_url = self.get_base_url(url)

            # Loop through all the links and get the href attribute
            for link in all_links:
                # Get the href attribute of the link
                href = link.get("href")
                # Create absolute URL if href is relative
                full_link = urllib.parse.urljoin(base_url, href)
                # Append each link as a separate list representing a row
                data.append([full_link])  # Add only the link for now

            # Print the number of links found on the page
            print(self.GREEN + f"Found {len(data)} links on {url}." + self.RESET)

            # Check for missing alt tags and capture the returned list
            missing_alt = self.check_missing_alt(all_links)

            # Check for missing aria labels and capture the returned list
            missing_aria = self.check_missing_aria(all_links)

            # Check for broken links
            self.check_broken_links([link[0] for link in data])  # Pass the extracted links to check_broken_links

            # Write data to Google Sheets
            self.write_to_google_sheets(data)  # Write extracted links to Google Sheets

            print("Scraping complete!\n")

            # Sort the data by type
            self.sort_data_by_type()
    
    def display_all_links(self):
        """
        Display all links scraped from the last webpage.
        """
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
        Sort the data by type.
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
            
            # Sort DataFrame by 'Type'
            df.sort_values(by="Type", inplace=True)

            # Update data in the worksheet
            self.write_to_google_sheets(df.values.tolist())
            
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
                if link.name == 'img' and not link.get('alt'):
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
                # Check for missing aria labels in anchor elements
                if link.name == 'a' and not link.get('aria-label'):
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

    def check_broken_links(self, links):
        """
        Check for broken links in the provided list of links.
        """
        print(self.CYAN + "Checking for broken links..." + self.RESET)
        broken_links = []
        valid_links = []
        # Load the existing data from Google Sheets
        try:
            data = self.WORKSHEET.get_all_values()
            print("Data from Google Sheets:", data)  # Debug print
            if not data:
                print("No links found in Google Sheets.")
                return
            else:
                # Construct DataFrame with explicit column names
                df = pd.DataFrame(data, columns=['Link URL'])
                print("DataFrame columns:", df.columns)  # Debug print

                # Add 'type' and 'status' columns if they don't exist
                if 'type' not in df.columns:
                    df['type'] = ''
                if 'status' not in df.columns:
                    df['status'] = ''

                # Rename the first column to 'Link URL' if not already
                if df.columns[0] != 'Link URL':
                    df.rename(columns={df.columns[0]: 'Link URL'}, inplace=True)

        except Exception as e:
            print("An unexpected error occurred:", str(e))
            return

        # Loop through all the links and check for broken links
        for link in tqdm(links, desc="Checking links", unit="link"):
            # Skip JavaScript void links
            if link.startswith("javascript:"):
                print(f"Skipping JavaScript void link: {link}")
                continue
            # Send a HEAD request to the link and check the status code
            try:
                response = requests.head(link, allow_redirects=True, timeout=5)
                if response.status_code >= 400:
                    print(f"Broken link found: {link}")
                    broken_links.append(link)
                else:
                    valid_links.append(link)
            except requests.exceptions.RequestException as e:
                print(self.RED + f"Error checking link {link}: {e}" + self.RESET)
                broken_links.append(link)

        # Update the status of links in the DataFrame
        df.loc[df['Link URL'].isin(broken_links), 'Status'] = 'broken'
        df.loc[df['Link URL'].isin(valid_links), 'Status'] = 'valid'

        try:
            # Write updated data to Google Sheets
            self.write_to_google_sheets(df.values.tolist())
        except Exception as e:
            print(self.RED + "Error updating Google Sheets:", e + self.RESET)

        if broken_links:
            print(self.RED + "Broken links found:" + self.RESET)
            for broken_link in broken_links:
                print(broken_link)
        else:
            print(self.GREEN + "No broken links found." + self.RESET)

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
                print("No broken links found.")
            else:
                print(self.RED + "Broken links found:" + self.RESET)
                for broken_link in broken_links['Link URL']:
                    print(broken_link)
        
        except Exception as e:
            print(self.ERROR_MESSAGE)

    def open_github(self):
        """
        Display the link to GitHub.
        """
        github_link = "https://github.com/jeffdruid/link-validator"
        print("\n" + self.GREEN + "GitHub link: " + github_link + self.RESET)
        try:
            os.system("start https://github.com/jeffdruid/link-validator")
            print("\n" + self.GREEN + "GitHub has been opened in a new tab." + self.RESET)
        except FileNotFoundError:
            print(self.RED + "\nFailed to open GitHub. Please check your internet connection." + self.RESET)

    def empty_links_google_sheet(self):
        """
        Empty the links Google Sheet.
        """
        try:
            # Clear existing data (including header)
            self.WORKSHEET.clear()
            print("\n" + self.GREEN + "The Google Sheet has been emptied." + self.RESET)
        except Exception as e:
            print(self.RED + "An unexpected error occurred:", str(e) + self.RESET)

    def ask_continue(self):
        """
        Ask the user if they want to continue.
        """
        while True:
            choice = input(self.YELLOW + "\nDo you want to continue? (y/n): " + self.RESET)
            if choice.lower() in ["y", "yes"]:
                self.main()
            elif choice.lower() in ["n", "no"]:
                print(self.RED + "\nExiting the program..." + self.RESET)
                exit()
            else:
                print(self.RED + "Invalid choice. Please enter 'y' or 'n'." + self.RESET)

    def main(self):
        """
        The main function of the Link-Validator Tool.
        """
        try:
            self.print_welcome_message()
            while True:
                self.print_instructions()
                
                choice = self.get_user_input()
                
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
                    print(self.RED + "\nNot implemented yet." + self.RESET)
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
