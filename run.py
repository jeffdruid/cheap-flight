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
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        for book in all_books:
            item = {}
            item["title"] = book.find("img").attrs["alt"]
            
            item["link"] = book.find("a").attrs["href"]
            
            item["price"] = book.find("p", class_="price_color").text[1:]
            
            print(item["price"])
            
        current_page += 1
        proceed = False