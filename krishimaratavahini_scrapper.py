#Released an official package to perform data scrappinh using kmvahini
pip install kmvahini
import kmvahini.scraper as scraper

# Define parameters for scraping
months = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER", "DECEMBER"]  # Specify months
years = [str(year) for year in range(2002, 2026)]
commodities = ["TOMATO"]  # Choose a commodity
markets = ["AllMarkets"]  # Select all or specific markets

# Scrape the data
df = scraper.scrape_website(months, years, commodities, markets)
output=df.to_csv('market_data_2002_2025.csv')
