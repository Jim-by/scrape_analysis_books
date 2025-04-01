import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Defining the project root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(SCRIPT_DIR, 'data', 'raw')
ANALYSIS_DATA_DIR = os.path.join(SCRIPT_DIR, 'data', 'analysis')

# Creating a directory if it does not exist
os.makedirs(ANALYSIS_DATA_DIR, exist_ok=True)

# Load data from JSON file
json_filename = "books.json"
json_path = os.path.join(RAW_DATA_DIR, json_filename)

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

#Flatten data into a single list of books
books = [{"category": category, **book} for category, books_list in data.items() for book in books_list]

# Convert data to Pandas DataFrame
df = pd.DataFrame(books)

# 1. Overview of data
print("Data Overview")
print(df.head())
print(df.info())
print(df.describe())

# 2. Handling missing values
print("\nMissing Values")
print(df.isnull().sum())

# 2.1 Fill in the missing values
df['description'] = df['description'].fillna('')
df['price'] = df['price'].fillna(0)
df['availability'] = df['availability'].fillna(0)

# 3. Price analysis
print("\nPrice Analysis")
print("Average price:", df['price'].mean())
print("Median price:", df['price'].median())
print("Highest price:", df['price'].max())
print("Lowest price", df['price'].min())

#3.1 Histogram of price distribution
plt.figure(figsize=(8,6))
sns.histplot(df['price'], bins=20, kde=True)
plt.title("Distribution of book prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.savefig(os.path.join(ANALYSIS_DATA_DIR, 'price_distribution.png'))
plt.show()

# 4. Availability analysis
print("\nAvailability Analysis")
print("Average quantity in stock:", df['availability'].mean())
print("Median quantity in stock:", df['availability'].median())

# 4.1 Are more books available or not?
available_books = df[df['availability'] > 0].shape[0]
unavailable_books = df[df['availability'] == 0].shape[0]
print(f"Books available: {available_books} ({available_books / df.shape[0] * 100:.2f}%)")
print(f"Anavailable books: {unavailable_books} ({unavailable_books / df.shape[0] * 100:.2f}%)")

# 5. Category analysis
print("\nCategory Analysis")
category_counts = df['category'].value_counts()
print(category_counts)

# 5.1 Barchart categories
plt.figure(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values)
plt.title("Number of books by category")
plt.xlabel("Category")
plt.ylabel("Quantity")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DATA_DIR, 'books_by_category.png'))

# 6. Price by Category
print("\nPrice by Category")
category_prices = df.groupby('category')['price'].agg(['mean', 'median', 'min', 'max'])
print(category_prices)

# 6.1 Boxplot prices by category
plt.figure(figsize=(12,8))
sns.boxplot(data=df, x='category', y='price')
plt.title("Price distribution by category")
plt.xlabel("Category")
plt.ylabel("Price")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_DATA_DIR, 'price_by_category.png'))
plt.show()

# 7. Correlation analysis (price vs availability)
print("\nCorrelation Analysis")
correlation = stats.pearsonr(df['price'], df['availability'])
print(f"Pearson correlation coefficient between price and availability: {correlation[0]:.4f} (p-value:{correlation[1]:.4f})")

# 7.1 Scatter plot (price vs availability)
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='price', y='availability')
plt.title("Correlation between price and availability")
plt.xlabel("Price")
plt.ylabel("Availability")
plt.savefig(os.path.join(ANALYSIS_DATA_DIR, 'price_vs_availability.png'))
plt.show()

# 8. The most expensive and cheapest books
print("\nTop 5 most expensive and cheapest books")
expensive_books = df.nlargest(5, 'price')[['title', 'price', 'category']]
cheap_books = df[df['price'] > 0].nsmallest(5, 'price')[['title', 'price', 'category']]
print("The most expensive books: ")
print(expensive_books)
print("\nThe cheapest books: ")
print(cheap_books)

# 9. Save the cleaned data for further analysis
cleaned_data_path = os.path.join(ANALYSIS_DATA_DIR, 'cleaned_books.csv')
df.to_csv(cleaned_data_path, index=False, encoding='utf-8')
print(f"\nCleaned data was saved into {cleaned_data_path}")

print("\nAnalysis completed.")