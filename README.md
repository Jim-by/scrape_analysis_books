## Books Scraping and Analysis Project
# Overview
This project involves scraping book data from the website books.toscrape.com and performing analysis on the collected data. The project consists of two main parts: data scraping and data analysis.

# Data Scraping
The data scraping part of the project uses Python libraries requests and BeautifulSoup to extract book data from the website. The scraped data includes book title, price, availability, and description. The data is stored in a JSON file named books.json.

# Data Analysis
The data analysis part of the project uses Python libraries pandas, numpy, matplotlib, and seaborn to analyze the collected data. The analysis includes:

* Overview of the data
* Handling missing values
* Price analysis (average, median, highest, and * lowest prices)
* Availability analysis (average and median availability)
* Category analysis (number of books by category)
* Price distribution by category
* Correlation analysis between price and availability
* Top 5 most expensive and cheapest books
# Requirements
To run the project, you need to install the following Python libraries:

requests
beautifulsoup4
pandas
numpy
matplotlib
seaborn
scipy

You can install the libraries using pip:
bash pip install -r requirements.txt
# Usage
1. Clone the repository: git clone https://github.com/your-username/books-scraping-analysis.git
2. Navigate to the project directory: cd books-scraping-analysis
3. Run the data scraping script: python src/scraping.py
4. Run the data analysis script: python src/analysis.py
# Results
The results of the analysis are stored in the data/analysis directory. The results include:

* cleaned_books.csv: cleaned data in CSV format
* price_distribution.png: histogram of price distribution
* books_by_category.png: bar chart of number of books by category
* price_by_category.png: box plot of price distribution by category
* price_vs_availability.png: scatter plot of correlation between price and availability
# License
This project is licensed under the MIT License. See the LICENSE file for details.