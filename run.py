import requests
from bs4 import BeautifulSoup

current_page = 1
proceed = True

while proceed:
    # Send a GET request to the website you want to scrape
    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"

    # Get the HTML content of the webpage
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the page exists
    if soup.title.text == "404 Not Found":
        proceed = False
    else:
        print("Scraping page", current_page)
        current_page += 1