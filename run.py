import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Back, Fore, Style
import os
import urllib.parse

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
        print("3. Display all duplicated links scraped from the last webpage")
        print("4. Sort the data in ascending order")
        print("5. Sort the data by type")
        print("6. Open the links.csv file in a new tab")
        print("7. Check for missing alt tags and aria labels in the scraped links")
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
                if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]:
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

    def scrape_and_validate_links(self):
        """
        Scrape and validate links from a webpage.
        """
        url = self.get_url_input()
        print("You entered: " + url)
        data = []

        # Print the current page being scraped
        print(f"\nScraping {url}...")

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
                data.append(full_link)

            # Print the number of links found on the page
            print(self.GREEN + f"Found {len(data)} links on {url}." + self.RESET)
            
            # Check for missing alt tags and aria labels
            self.check_missing_alt_aria(all_links)
            
            # Check for broken links
            self.check_broken_links(data)

            # Convert the list to a DataFrame and save it to a CSV file
            df = pd.DataFrame(data, columns=["link"])
            df.to_csv("links.csv", index=False)
            print("Scraping complete!\n")

    def display_all_links(self):
        """
        Display all links scraped from the last webpage.
        """
        if os.path.isfile("links.csv"):
            try:
                # Load the CSV file containing links
                df = pd.read_csv("links.csv")
                if df.empty:
                    print("No links found.")
                else:
                    print(df)
            except FileNotFoundError:
                print(self.ERROR_MESSAGE)
            except pd.errors.EmptyDataError:
                print(self.ERROR_MESSAGE)
        else:
            print("No links.csv file found.")

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

    def display_duplicated_links(self):
        """
        Display all duplicated links scraped from the last webpage.
        """
        print(self.RED + "This feature is not yet implemented. REMOVED" + self.RESET)
        # try:
        #     # Load the CSV file containing links
        #     df = pd.read_csv("links.csv")
        #     duplicated_links = df[df.duplicated(subset="link")]
        #     print("\n" + self.GREEN + "Duplicated links:" + self.RESET + " " + str(len(duplicated_links)))
        # except FileNotFoundError:
        #     print(self.ERROR_MESSAGE)
        # except pd.errors.EmptyDataError:
        #     print(self.ERROR_MESSAGE)

    def sort_data(self):
        """
        Sort the data in ascending order.
        """
        print(self.RED + "This feature is not yet implemented. REMOVED" + self.RESET)
        # try:
        #     # Load the CSV file containing links
        #     df = pd.read_csv("links.csv")
        #     df.sort_values(by="link", inplace=True)
        #     df.to_csv("links.csv", index=False)
        #     print("\n" + self.GREEN + "Data sorted successfully." + self.RESET)
        # except FileNotFoundError:
        #     print(self.ERROR_MESSAGE)
        # except pd.errors.EmptyDataError:
        #     print(self.ERROR_MESSAGE)

    def sort_data_by_type(self):
        """
        Sort the data by type.
        """
        try:
            # Load the CSV file containing links
            df = pd.read_csv("links.csv")
            df['type'] = df['link'].apply(self.get_link_type)
            df.sort_values(by="type", inplace=True)
            df.to_csv("links.csv", index=False)
            print("\n" + self.GREEN + "Data sorted by type successfully." + self.RESET)
        except FileNotFoundError:
            print(self.ERROR_MESSAGE)
        except pd.errors.EmptyDataError:
            print(self.ERROR_MESSAGE)

    def get_link_type(self, link):
        """
        Get the type of the link.
        """
        if link.startswith("http://") or link.startswith("https://"):
            return "external"
        else:
            return "internal"

    def open_links_csv(self):
        """
        Open the links.csv file in a new tab.
        """
        
        try:
            os.system("start links.csv")
            print("\n" + self.GREEN + "The links.csv file has been opened in a new tab." + self.RESET)
        except FileNotFoundError:
            print(self.ERROR_MESSAGE)

    def check_missing_alt_aria(self, all_links):
        """
        Check for missing alt tags and aria labels in the scraped links.
        """
        try:
            # Initialize lists to store links with missing alt tags and aria labels
            missing_alt = []
            missing_aria = []

            # Loop through all links
            for link in all_links:
                # Check for missing alt tags in img elements
                if link.name == 'img' and not link.get('alt'):
                    missing_alt.append(link)

                # Check for missing aria labels in anchor elements
                if link.name == 'a' and not link.get('aria-label'):
                    missing_aria.append(link)

            # Print links with missing alt tags
            print("\n" + self.GREEN + "Number of links with missing alt tags: " + str(len(missing_alt)) + self.RESET)
            
            # TODO - Move this to display missing alt tags
            # if missing_alt:
            #     print("\n" + self.GREEN + "Links with missing alt tags:" + self.RESET)
            #     for link in missing_alt:
            #         print(link)

            # Print links with missing aria labels
            print("\n" + self.GREEN + "Number of links with missing aria labels: " + str(len(missing_aria)) + self.RESET)
            
            # TODO - Move this to display missing aria labels
            # if missing_aria:
            #     print("\n" + self.GREEN + "Links with missing aria labels:" + self.RESET)
            #     for link in missing_aria:
            #         print(link)
        except Exception as e:
            print("Error:", e)

    def check_broken_links(self, links):
        """
        Check for broken links in the provided list of links.
        """
        print(self.CYAN + "Checking for broken links..." + self.RESET)
        broken_links = []
        for link in tqdm(links, desc="Checking links", unit="link"):
            if link.startswith("javascript:"):
                print(f"Skipping JavaScript void link: {link}")
                continue
            try:
                response = requests.head(link, allow_redirects=True, timeout=5)
                if response.status_code >= 400:
                    print(f"Broken link found: {link}")
                    broken_links.append(link)
            except requests.exceptions.RequestException as e:
                print(self.RED + f"Error checking link {link}: {e}" + self.RESET)
                broken_links.append(link)
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
            # Load the CSV file containing links
            df = pd.read_csv("links.csv")
            if df.empty:
                print("No links found.")
            else:
                self.check_broken_links(df['link'])
        except FileNotFoundError:
            print(self.ERROR_MESSAGE)
        except pd.errors.EmptyDataError:
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

    def display_error_message(self):
        """
        Display an error message if the links.csv file is not found.
        """
        print(self.RED + "\nNo links found. Please scrape a webpage first." + self.RESET)
        
    def empty_links_csv(self):
        """
        Empty the links.csv file.
        """
        try:
            open("links.csv", "w").close()
            print("\n" + self.GREEN + "The links.csv file has been emptied." + self.RESET)
        except FileNotFoundError:
            print(self.ERROR_MESSAGE)
        except pd.errors.EmptyDataError:
            print(self.ERROR_MESSAGE)

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
                    self.display_duplicated_links()
                elif choice == 4:
                    self.sort_data()
                elif choice == 5:
                    self.sort_data_by_type()
                elif choice == 6:
                    self.open_links_csv()
                elif choice == 7:
                    self.check_missing_alt_aria()
                elif choice == 8:
                    self.display_broken_links()
                elif choice == 9:
                    self.open_github()
                elif choice == 10:
                    self.empty_links_csv()
                elif choice == 0:
                    print(self.RED + "\nExiting the program..." + self.RESET)
                    exit()
                self.ask_continue()
        except KeyboardInterrupt:
            print(self.RED + "\nProgram terminated by user." + self.RESET)
            exit()

if __name__ == "__main__":
    link_validator = LinkValidator()
    link_validator.main()
