from src.xbox_scrapper import scrape_deals_in_page
import os

deals = scrape_deals_in_page()

csv_path = os.path.join("data", "xbox_deals.csv")
deals.to_csv(csv_path, index=False, encoding="utf-8")