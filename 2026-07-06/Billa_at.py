
import csv

import requests

from parsel import Selector

main_sitemap = "https://shop.billa.at/sitemap.xml"

headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
}

try:

    respoanse = requests.get(main_sitemap, headers = headers)

    doc_tree =  Selector(text= respoanse.text, type="xml")

    sub_sitemaps = doc_tree.xpath("//*[local-name()='loc']/text()").getall()

    # print(sub_sitemaps)

    # pdp

    # for sub_urls in sub_sitemaps:

    product_sitemaps = [s for s in sub_sitemaps if 'produkte' in s.lower() or 'pdp' in s.lower()]

    pdp_url = list(set(product_sitemaps))

    output_file = "billa_at_pdp_url.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
       writer = csv.writer(f)
    
    # Optional: Add a header row so you know what the column is
       writer.writerow(["PDP_URL"]) 
    
    # Write each URL as a separate row
       for url in pdp_url:
          writer.writerow([url])

except Exception as e:

    pass

# https://shop.billa.at/api/product-discovery/products/search/%22%20%22?sortBy=relevance&enableStatistics=true&enablePersonalization=false&page=0&pageSize=30