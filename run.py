import requests
from bs4 import BeautifulSoup

# Send a GET request to the website you want to scrape
url = "https://books.toscrape.com/catalogue/page-1.html"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

print(soup.title.text)

# Find and extract the desired data from the HTML
# For example, let's extract all the links on the page
# links = soup.find_all("a")
# for link in links:
    # print(link.get("href"))