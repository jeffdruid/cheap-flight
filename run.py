import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import colorama
from colorama import Fore, Style
import webbrowser

colorama.init()  # Initialize colorama
print(Fore.GREEN + "\nWelcome to the Link-Validator Tool!\n" + Style.RESET_ALL)
print(Fore.YELLOW + "This tool allows you to scrape a webpage and validate all the links." + Style.RESET_ALL)
    
def print_instructions():
    """
    Display the instructions for using the Link-Validator Tool.
    """    
    print("\nPlease select an option from the menu below:")
    print(Fore.CYAN + "1. Scrape and validate links from a webpage")
    print("2. Display all links scraped from the last webpage")
    print("3. Display all duplicated links scraped from the last webpage")
    print("4. Sort the data in ascending order")
    print("5. Sort the data by type")
    print("6. Open the links.csv file in a new tab")
    print("7. Check for missing alt tags and aria labels in the scraped links")
    print("8. Check for broken links (Coming soon)")
    print("9. Open GitHub")
    print("0. Exit" + Style.RESET_ALL)
    print("")

def get_user_input():
    """
    Get the user's menu choice.
    """
    while True:
        try:
            choice = int(input(Fore.YELLOW + "Enter your choice (1, 2, 3, 4, 5, 6, 7, 8, 9 or 0): " + Style.RESET_ALL))
            if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
                return choice
            else:
                print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9 or 0.\n" + Style.RESET_ALL)
        except ValueError:
            print("Invalid input. Please enter a number.")

def scrape_and_validate_links():
    """
    Scrape and validate links from a webpage.
    """
    url = get_url_input()
    print("You entered: " + url)
    data = []

    # Print the current page being scraped
    print(f"Scraping {url}...")

    # Load the webpage and parse the HTML content
    soup = load_page_with_progress(url)

    if soup:
        # Find all the links on the page
        all_links = soup.find_all("a")

        # Loop through all the links and get the href attribute
        for link in all_links:
            # Get the href attribute of the link
            href = link.get("href")
            data.append(href)

        # Print the number of links found on the page
        print(f"Found {len(data)} links on {url}.")

        # Convert the list to a DataFrame and save it to a CSV file
        df = pd.DataFrame(data, columns=["link"])
        df.to_csv("links.csv", index=False)
        print("Scraping complete!\n")

def display_all_links():
    """
    Display all links scraped from the last webpage.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        print(df)
    except FileNotFoundError:
        print("No links found. Please scrape a webpage first.")
        
def get_url_input():
    """
    Get the URL input from the user and validate it.
    """
    while True:
        try:
            url = input("\nEnter the URL you want to scrape: \n")
            # Check if the URL starts with "http://" or "https://"
            if not url.startswith(("http://", "https://")):
                # If not, add "http://" to the beginning of the URL
                url = "https://" + url
            if validate_url(url):
                return url
            else:
                print("Invalid URL. Please try again.")
        except KeyboardInterrupt:
            print("\nProgram terminated by user.")
            exit()

def validate_url(url):
    """
    Validate the URL by sending a HEAD request and checking the status code.
    """
    try:
        response = requests.head(url, allow_redirects=True, stream=True, timeout=5)
        print("Status code: " + str(response.status_code))
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False
    except ValueError as e:
        print(f"Invalid URL: {e}")
        return False

def load_page_with_progress(url):
    """
    Load a webpage and display a progress bar while loading.
    """
    try:
        # Get the HTML content of the webpage
        response = requests.get(url, stream=True)

        # Store the response content in a variable
        html_content = response.content

        # Display the progress bar while reading the content
        with tqdm(total=len(html_content), unit="B", unit_scale=True, desc="Loading", unit_divisor=2048) as progress_bar:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def display_duplicated_links():
    """
    Display all duplicated links scraped from the last webpage.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        duplicated_links = df[df.duplicated(subset="link")]
        print("\n" + Fore.GREEN + "Duplicated links:" + Style.RESET_ALL + " " + str(len(duplicated_links)))
    except FileNotFoundError:
        print("\nNo links found. Please scrape a webpage first.")

def sort_data():
    """
    Sort the data in ascending order.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        df.sort_values(by="link", inplace=True)
        df.to_csv("links.csv", index=False)
        print("\n" + Fore.GREEN + "Data sorted successfully." + Style.RESET_ALL)
    except FileNotFoundError:
        print("\nNo links found. Please scrape a webpage first.")

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
        print("\n" + Fore.GREEN + "Data sorted by type successfully." + Style.RESET_ALL)
    except FileNotFoundError:
        print("\nNo links found. Please scrape a webpage first.")

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
                webbrowser.open_new_tab("links.csv")
                print("\n" + Fore.GREEN + "The links.csv file has been opened in a new tab." + Style.RESET_ALL)
            except FileNotFoundError:
                print("\nNo links found. Please scrape a webpage first.")

def check_missing_alt_aria():
    """
    Check for missing alt tags and aria labels in the scraped links.
    """
    try:
        # Load the CSV file containing links
        df = pd.read_csv("links.csv")
        
        # Check for missing alt tags
        missing_alt = df[df["link"].str.contains("<img") & ~df["link"].str.contains("alt=")]
        print("\n" + Fore.GREEN + "Links with missing alt tags:" + Style.RESET_ALL)
        print(missing_alt)
        
        # Check for missing aria labels
        missing_aria = df[df["link"].str.contains("<a") & ~df["link"].str.contains("aria-label=")]
        print("\n" + Fore.GREEN + "Links with missing aria labels:" + Style.RESET_ALL)
        print(missing_aria)
    except FileNotFoundError:
        print("\nNo links found. Please scrape a webpage first.")
   
def open_github():
    """
    Open GitHub in a new tab.
    """
    try:
        webbrowser.open_new_tab("https://github.com/jeffdruid/link-validator")
        print("\n" + Fore.GREEN + "GitHub has been opened in a new tab." + Style.RESET_ALL)
    except FileNotFoundError:
        print("\nFailed to open GitHub. Please check your internet connection.")

def main():
    """
    The main function of the Link-Validator Tool.
    """
    try:
        print_instructions()
        choice = get_user_input()
        
        if choice == 1:
            scrape_and_validate_links()
            main()
        elif choice == 2:
            display_all_links()
            main()
        elif choice == 3:
            display_duplicated_links()
            main()
        elif choice == 4:
            sort_data()
            main()
        elif choice == 5:
            sort_data_by_type()
            main()
        elif choice == 6:
            open_links_csv()
            main()
        elif choice == 7:
            check_missing_alt_aria()
            main()
        elif choice == 9:
            open_github()
            main()
        elif choice == 0:
            print(Fore.RED + "\nExiting the program..." + Style.RESET_ALL)
            exit()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram terminated by user." + Style.RESET_ALL)
        exit()

# TODO - Add link validation to check if the link is valid
# TODO - check for broken links
# TODO - check for redirects

if __name__ == "__main__":
    main()