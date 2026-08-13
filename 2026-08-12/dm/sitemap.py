
import requests

import csv

from parsel import Selector

main_sitemap =  "https://www.dm.hu/sitemap.xml"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try :

    respoanse = requests.get(main_sitemap, headers = headers)

    doc_tree =  Selector(text= respoanse.text, type="xml")

    

    sub_sitemaps = doc_tree.xpath("//*[local-name()='loc']/text()").getall()

    

    product_sitemaps = [s for s in sub_sitemaps if 'product' in s.lower() or 'pdp' in s.lower()]

    # print(product_sitemaps)

    if not product_sitemaps:

        print("not found")
    
    pdp_urls = []

    for sub_products in product_sitemaps:

        sub_respoanse = requests.get(sub_products, headers = headers)

        sub_tree = Selector(text= sub_respoanse.text, type = "xml")

        # print(sub_tree)

        all_links = sub_tree.xpath("//*[local-name()='loc']/text()").getall()

        for links in all_links:

            if "/p/d/" in links:

                pdp_urls.append(links)

    

    output_file = "dm_si_pdp_urls.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
       writer = csv.writer(f)
    
    
       writer.writerow(["PDP_URL"]) 
    
    
       for url in pdp_urls:
          writer.writerow([url])

except Exception as e:

    print(f"error{e}")

