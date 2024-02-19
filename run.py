import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1
data = []
proceed = True
url = input("Enter the URL you want to scrape: ")

# Check if the URL is allowed to be scraped by robots.txt
robots_url = url + "/robots.txt"
robots_response = requests.get(robots_url)
robots_content = robots_response.text

if "User-agent: *" in robots_content and "Disallow: /" in robots_content:
    print("This website does not allow scraping.")
    print("Please check the robots.txt file for more information.")
    print(robots_url)
    proceed = False
else:
    # If the website allows scraping, proceed with the scraping
    
    # Print the current page being scraped
    print(f"Scraping page {current_page}...")

    # Get the HTML content of the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the links on the page
    all_links = soup.find_all("a")
    
    # Loop through all the links and get the href attribute
    for link in all_links:
        # Get the href attribute of the link
        href = link.get("href")
        data.append(href)
    
    # Print the number of links found on the page
    print(f"Found {len(data)} links on page {current_page}.")
                    
# Convert the list to a DataFrame and save it to a CSV file
df = pd.DataFrame(data, columns=["link"])
df.to_csv("links.csv", index=False)
print("Scraping complete!")

# Sort the data
# data.sort()

# test - URL: https://jeffdruid.github.io/fitzgeralds-menu/menu

# TODO - Add a function to check if the URL is valid
# TODO - Add a function to sort the data
# TODO - Add a function to display the data
# TODO - Add a function to search the data
# TODO - Add a function to filter the data
# TODO - Add a function to handle errors
# TODO - Add a function to handle exceptions
# TODO - Add a function to handle pagination
# TODO - Add a function to handle proxies
# TODO - Add a function to handle user agents
# TODO - Add a function to handle status codes
# TODO - Add a function to handle rate limits
# TODO - Add a function to handle timeouts