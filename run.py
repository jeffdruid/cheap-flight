import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Back, Fore, Style
import os
import urllib.parse

#constants
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
WHITE = Fore.WHITE
BLACK = Fore.BLACK

RESET = Style.RESET_ALL

ERROR_MESSAGE = (RED + "\nNo links found. Please scrape a webpage first." + RESET)

def initialize_colorama():
    """
    Initialize colorama and set the color for the welcome message.
    """
    colorama.init()

initialize_colorama()

def print_welcome_message():
    """
    Print the welcome message for the Link-Validator Tool.
    """
    print(Style.BRIGHT + Back.GREEN + WHITE + "\nWelcome to the Link-Validator Tool!\n" + RESET + YELLOW + "\nThis tool allows you to scrape a webpage and validate all the links." + RESET)

print_welcome_message()

def print_instructions():
    """
    Display the instructions for using the Link-Validator Tool.
    """    
    print(MAGENTA + "\nPlease select an option from the menu below:")
    print(CYAN + "1. Scrape and validate links from a webpage")
    print("2. Display all links scraped from the last webpage")
    print("3. Display all duplicated links scraped from the last webpage")
    print("4. Sort the data in ascending order")
    print("5. Sort the data by type")
    print("6. Open the links.csv file in a new tab")
    print("7. Check for missing alt tags and aria labels in the scraped links")
    print("8. Display broken links from the last webpage")
    print("9. Open GitHub")
    print("0. Exit" + RESET)
    print("")

def get_user_input():
    """
    Get the user's menu choice.
    """
    while True:
        try:
            choice = int(input(YELLOW + "Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): " + RESET))
            if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]:
                return choice
            else:
                print(RED + "Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9 or 0.\n" + RESET)
        except ValueError:
            print(RED + "Invalid input. Please enter a number." + RESET)

def get_base_url(url):
    """
    Extract the base URL from the given URL.
    """
    parsed_url = urllib.parse.urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url

def scrape_and_validate_links():
    """
    Scrape and validate links from a webpage.
    """
    url = get_url_input()
    print("You entered: " + url)
    data = []

    # Print the current page being scraped
    print(f"\nScraping {url}...")
    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    if soup:
        # Find all the links on the page
        all_links = soup.find_all("a")
        
        # Extract base URL
        base_url = get_base_url(url)
    
        # Loop through all the links and get the href attribute
        for link in all_links:
            # Get the href attribute of the link
            href = link.get("href")
            # Create absolute URL if href is relative
            full_link = urllib.parse.urljoin(base_url, href)
            data.append(full_link)

        # Print the number of links found on the page
        print(GREEN + f"Found {len(data)} links on {url}." + RESET)
        
        # Check for missing alt tags and aria labels
        check_missing_alt_aria(all_links)
        
        # Check for broken links
        check_broken_links(data)

        # Convert the list to a DataFrame and save it to a CSV file
        df = pd.DataFrame(data, columns=["link"])
        df.to_csv("links.csv", index=False)
        print("Scraping complete!\n")

def display_all_links():
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
            print(ERROR_MESSAGE)
        except pd.errors.EmptyDataError:
            print(ERROR_MESSAGE)
    else:
        print("No links.csv file found.")
        
def get_url_input():
    """
    Get the URL input from the user and validate it.
    """
    while True:
        try:
            url = input(CYAN + "\nEnter the URL you want to scrape: \n" + RESET)
            # Check if the URL starts with "http://" or "https://"
            if not url.startswith(("http://", "https://")):
                # If not, add "http://" to the beginning of the URL
                url = "https://" + url
            if validate_url(url):
                return url
            else:
                print(RED + "Invalid URL. Please try again." + RESET)
        except KeyboardInterrupt:
            print(RED + "\nProgram terminated by user." + RESET)
            exit()

def validate_url(url):
    """
    Validate the URL by sending a HEAD request and checking the status code.
    """
    try:
        response = requests.head(url, allow_redirects=True, stream=True, timeout=5)
        print(GREEN + "Status code: " + str(response.status_code) + RESET)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(Back.RED + f"Error: {e}" + RESET)
        return False
    except ValueError as e:
        print(f"Invalid URL: {e}")
        return False

def display_duplicated_links():
    """
    Display all duplicated links scraped from the last webpage.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        duplicated_links = df[df.duplicated(subset="link")]
        print("\n" + GREEN + "Duplicated links:" + RESET + " " + str(len(duplicated_links)))
    except FileNotFoundError:
        print(ERROR_MESSAGE)
    except pd.errors.EmptyDataError:
        print(ERROR_MESSAGE)

def sort_data():
    """
    Sort the data in ascending order.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        df.sort_values(by="link", inplace=True)
        df.to_csv("links.csv", index=False)
        print("\n" + GREEN + "Data sorted successfully." + RESET)
    except FileNotFoundError:
        print(ERROR_MESSAGE)
    except pd.errors.EmptyDataError:
        print(ERROR_MESSAGE)

def sort_data_by_type():
    """
    Sort the data by type.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        df['type'] = df['link'].apply(get_link_type)
        df.sort_values(by="type", inplace=True)
        df.to_csv("links.csv", index=False)
        print("\n" + GREEN + "Data sorted by type successfully." + RESET)
    except FileNotFoundError:
        print(ERROR_MESSAGE)
    except pd.errors.EmptyDataError:
        print(ERROR_MESSAGE)

def get_link_type(link):
    """
    Get the type of the link.
    """
    if link.startswith("http://") or link.startswith("https://"):
        return "external"
    else:
        return "internal"

def open_links_csv():
            """
            Open the links.csv file in a new tab.
            """
            
            try:
                os.system("start links.csv")
                print("\n" + GREEN + "The links.csv file has been opened in a new tab." + RESET)
            except FileNotFoundError:
                print(ERROR_MESSAGE)

def check_missing_alt_aria(all_links):
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
        if missing_alt:
            print("\n" + GREEN + "Links with missing alt tags:" + RESET)
            for link in missing_alt:
                print(link)

        # Print links with missing aria labels
        if missing_aria:
            print("\n" + GREEN + "Links with missing aria labels:" + RESET)
            for link in missing_aria:
                print(link)
    except Exception as e:
        print("Error:", e)

def check_broken_links(links):
    """
    Check for broken links in the provided list of links.
    """
    print(CYAN + "Checking for broken links..." + RESET)
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
            print(RED + f"Error checking link {link}: {e}" + RESET)
            broken_links.append(link)
    if broken_links:
        print(RED + "Broken links found:" + RESET)
        for broken_link in broken_links:
            print(broken_link)
    else:
        print(GREEN + "No broken links found." + RESET)

def display_broken_links():
    """
    Display broken links from the last webpage.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        if df.empty:
            print("No links found.")
        else:
            check_broken_links(df['link'])
    except FileNotFoundError:
        print(ERROR_MESSAGE)
    except pd.errors.EmptyDataError:
        print(ERROR_MESSAGE)

def open_github():
    """
    Display the link to GitHub.
    """
    github_link = "https://github.com/jeffdruid/link-validator"
    print("\n" + GREEN + "GitHub link: " + github_link + RESET)
    try:
        os.system("start https://github.com/jeffdruid/link-validator")
        print("\n" + GREEN + "GitHub has been opened in a new tab." + RESET)
    except FileNotFoundError:
        print(RED + "\nFailed to open GitHub. Please check your internet connection." + RESET)

def display_error_message():
    """
    Display an error message if the links.csv file is not found.
    """
    print(RED + "\nNo links found. Please scrape a webpage first." + RESET)
    
def empty_links_csv():
    """
    Empty the links.csv file.
    """
    try:
        open("links.csv", "w").close()
        print("\n" + GREEN + "The links.csv file has been emptied." + RESET)
    except FileNotFoundError:
        print(ERROR_MESSAGE)
    except pd.errors.EmptyDataError:
        print(ERROR_MESSAGE)

def ask_continue():
    """
    Ask the user if they want to continue.
    """
    while True:
        choice = input(YELLOW + "\nDo you want to continue? (y/n): " + RESET)
        if choice.lower() in ["y", "yes"]:
            main()
        elif choice.lower() in ["n", "no"]:
            print(RED + "\nExiting the program..." + RESET)
            exit()
        else:
            print(RED + "Invalid choice. Please enter 'y' or 'n'." + RESET)

def main():
    """
    The main function of the Link-Validator Tool.
    """
    try:
        print_instructions()
        choice = get_user_input()
        
        if choice == 1:
            scrape_and_validate_links()
            ask_continue()
        elif choice == 2:
            display_all_links()
            ask_continue()
        elif choice == 3:
            display_duplicated_links()
            ask_continue()
        elif choice == 4:
            sort_data()
            ask_continue()
        elif choice == 5:
            sort_data_by_type()
            ask_continue()
        elif choice == 6:
            open_links_csv()
            ask_continue()
        elif choice == 7:
            check_missing_alt_aria()
            ask_continue()
        elif choice == 8:
            display_broken_links()
            ask_continue()
        elif choice == 9:
            open_github()
            ask_continue()
        elif choice == 10:
            empty_links_csv()
            ask_continue()
        elif choice == 0:
            print(RED + "\nExiting the program..." + RESET)
            exit()
    except KeyboardInterrupt:
        print(RED + "\nProgram terminated by user." + RESET)
        exit()

if __name__ == "__main__":
    main()