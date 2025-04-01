import os
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import re

# Defining the project root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(SCRIPT_DIR, 'data', 'raw')

# Creating a directory if it does not exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# Initialize UserAgent
ua = UserAgent()
headers = {"User-Agent": ua.chrome}

# Base URL of the website
base_url = "http://books.toscrape.com/"

# Function to get all book categories
def get_categories(soup):
    categories = {}
    for category in soup.select(".side_categories ul li a"):
        if 'books_1' not in category['href']:  # Skip main category
            categories[category.text.strip()] = base_url + category['href']
    return categories

# Function to extract book data
def get_book_data(book_url):
    response = requests.get(book_url, headers=headers)
    book_soup = BeautifulSoup(response.text, features="html.parser")

    title = book_soup.find("h1").text

    price_tag = book_soup.select_one(".price_color")
    if price_tag:
        price_text = price_tag.text.strip()
        price = float(re.sub(r'[^\d.]', '', price_text))  # Remove everything except digits and dot
    else:
        price = None  # If price not found

    availability_tag = book_soup.select_one(".availability")
    if availability_tag:
        availability_text = availability_tag.text.strip()
        match = re.search(r'\d+', availability_text)
        if match:
            availability = int(match.group())  # Extract number
        else:
            availability = None  # If quantity not found
    else:
        availability = None

    description_tag = book_soup.find("meta", attrs={"name": "description"})
    if description_tag and description_tag["content"].strip():
        description = description_tag["content"].strip()
    else:
        description = None  # If description not found

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "description": description
    }

# Function to process category page
def process_category_page(url):
    books = []
    while url:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")

        for book in soup.select(".product_pod"):
            book_url = base_url + "catalogue/" + book.select_one("h3 a")["href"].replace("../", "")
            books.append(get_book_data(book_url))

        next_page = soup.select_one(".next a")
        if next_page:
            url = base_url + next_page["href"]
        else:
            url = None

    return books

# Main process
def main():
    # Getting the list of categories
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    categories = get_categories(soup)

    # Data collection by category
    all_books = {}
    for category, url in categories.items():
        print(f"Processing category: {category}")
        all_books[category] = process_category_page(url)

    # Path for saving JSON file
    json_filename = "books.json"
    json_path = os.path.join(RAW_DATA_DIR, json_filename)

    # Data storage
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_books, f, ensure_ascii=False, indent=4)

    print(f"Data saved to {json_path}")
    print(f"Total categories processed: {len(categories)}")
    print(f"Total books collected: {sum(len(books) for books in all_books.values())}")

if __name__ == "__main__":
    main()