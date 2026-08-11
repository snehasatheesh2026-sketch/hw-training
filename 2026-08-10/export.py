import csv
import logging
import json
from settings import (
    MONGO_COLLECTION_CATEGORY,
    file_name,
    FILE_HEADERS,
    client,
    MONGO_DB
)


from bs4 import BeautifulSoup

seen_urls = set()
count = 0
with open(
    "matalanme_2026_08_11_sample.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(FILE_HEADERS)
    
    for item in client[MONGO_DB][MONGO_COLLECTION_CATEGORY].find(
        no_cursor_timeout=True
    ):
        url = item.get("url", "")
        if url in seen_urls:
            print(f"Duplicate URL skipped: {url}")
            continue
        seen_urls.add(url)

        from datetime import datetime

        # extraction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")






        # product_name = item.get("product_name", "")
        # colors = item.get("colors", "")
        # stock_status = item.get('stock_status','')
        # sizes = item.get("sizes", "")
        # url = item.get("url", "")
        # images = item.get("images", "")
        # product_id = item.get("product_id", "")
        # sellings_price = item.get("sellings_price", "")
        # currency = item.get("currency", "")
        # regular_price = item.get("regular_price", "")
        # gender = item.get("gender", "")
        # product_details = item.get("product_details", "")
        # description = item.get("description", "")
        # breadcrumb = item.get("breadcrumb","")
        # quantity = item.get("quantity",'')
        url = item.get("url", "") 
        product_id = item.get("product_id", "")
        product_name = item.get("product_name", "")
        extraction_date = item.get("extraction_date","")
        regular_price = item.get("regular_price", "")
        sellings_price = item.get("sellings_price", "")
        currency = item.get("currency", "")
        description = item.get("description", "")
        breadcrumb = item.get("breadcrumb", "")
        quantity = item.get("quantity", "")
        product_details = item.get("product_details", "")
        colors = item.get("colors", "")
        sizes = item.get("sizes", "")
        gender = item.get("gender", "")
        images = item.get("images", "")

        if description:
            soup = BeautifulSoup(description, "html.parser")
            description = soup.get_text(" ", strip=True)
        



        if count == 200:
           break
        data = [
    url,
    product_id,
    product_name,
    extraction_date,
    regular_price,
    sellings_price,
    currency,
    description,
    breadcrumb,
    quantity,
    product_details,
    colors,
    sizes,
    gender,
    images,
]

        
  


        writer.writerow(data)
        count += 1

print("CSV exported successfully.")

