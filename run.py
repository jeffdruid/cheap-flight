import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1
data = []
proceed = True

while proceed:
    # Print the current page being scraped
    print(f"Scraping page {current_page}...")
    
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
        # Find all the books on the page
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        # Loop through each book and get the title, link, price, and stock
        for book in all_books:
            item = {}
            
            item["title"] = book.find("img").attrs["alt"]
            
            item["link"] = book.find("a").attrs["href"]
            
            item["price"] = book.find("p", class_="price_color").text[1:]
            
            item["stock"] = book.find("p", class_="instock availability").text.strip()
            
            # Append the data to the list
            data.append(item)
            
        current_page += 1
        
## Convert the list to a DataFrame and save it to a CSV file
df = pd.DataFrame(data)
df.to_csv("books.csv", index=False)