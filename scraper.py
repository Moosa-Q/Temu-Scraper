# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

# import scraperwiki
# import lxml.html
#
# # Read in a page
# html = scraperwiki.scrape("http://foo.com")
#
# # Find something on the page using css selectors
# root = lxml.html.fromstring(html)
# root.cssselect("div[align='left']")
#
# # Write out to the sqlite database using scraperwiki library
# scraperwiki.sqlite.save(unique_keys=['name'], data={"name": "susan", "occupation": "software developer"})
#
# # An arbitrary query against the database
# scraperwiki.sql.select("* from data where 'name'='peter'")

# You don't have to do things with the ScraperWiki and lxml libraries.
# You can use whatever libraries you want: https://morph.io/documentation/python
# All that matters is that your final data is written to an SQLite database
# called "data.sqlite" in the current working directory which has at least a table
# called "data".


import requests
from bs4 import BeautifulSoup
import sqlite3

# Connect to SQLite database (Morph.io uses SQLite)
conn = sqlite3.connect("data.sqlite")
cursor = conn.cursor()

# Create a table to store the data
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price TEXT
)
""")

def scrape_temu(search_term):
    # Build the search URL
    url = f"https://www.temu.com/search?q={search_term.replace(' ', '+')}"

    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send GET request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the page. Status Code:", response.status_code)
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find products
    products = soup.find_all("div", class_="product-item")  # Adjust class name based on Temu's structure
    for product in products:
        title = product.find("a", class_="product-title")
        price = product.find("span", class_="price-current")

        if title and price:
            # Extract and clean text
            title_text = title.get_text(strip=True)
            price_text = price.get_text(strip=True)

            # Print and save to the database
            print(f"Product: {title_text} - Price: {price_text}")
            cursor.execute("INSERT INTO products (title, price) VALUES (?, ?)", (title_text, price_text))

    # Commit changes to the database
    conn.commit()

if __name__ == "__main__":
    search_term = "iphone case"  # Change this to any search term
    scrape_temu(search_term)
    conn.close()

