import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def print_instructions():
    """
    Display the instructions for using the Link-Validator Tool.
    """
    print("\nWelcome to the Link-Validator Tool!\n")
    print("This tool allows you to scrape a webpage and validate all the links.\n")
    print("Please select an option from the menu below:")
    print("1. Scrape and validate links from a webpage")
    print("2. Display all links scraped from the last webpage")
    print("0. Exit")
    print("")

def get_user_input():
    """
    Get the user's menu choice.
    """
    while True:
        try:
            choice = int(input("Enter your choice (1, 2 or 0): "))
            if choice in [1, 2, 0]:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2 or 0.")
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
        print("Scraping complete!")

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
        elif choice == 0:
            print("Exiting the program...")
            exit()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        exit()

    
# Sort the data
# data.sort()

# test - URL: https://jeffdruid.github.io/fitzgeralds-menu/menu

# TODO - Add link validation to check if the link is valid
# TODO - Add filtering to remove duplicate links
# TODO - Add filtering types (e.g. only internal links, only external links)
# TODO - Add a function to save the data to a file
# TODO - Add a function to load the data from a file
# TODO - Add a function to handle different types of data (e.g. images, videos, text)
# TODO - Add error handling for requests where url is invalid or inaccessible
# TODO - Add a function to sort the data
# TODO - Add a function to display the data
# TODO - Add a function to search the data
# TODO - Add a function to filter the data
# TODO - Add a function to handle pagination
# TODO - Add a function to handle proxies
# TODO - Add a function to handle user agents
# TODO - Add a function to handle rate limits
# TODO - Add a function to handle timeouts

if __name__ == "__main__":
    main()