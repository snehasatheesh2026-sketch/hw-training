
##############################CRAWLER##############################

import requests
import json
import re

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en;q=0.9',
    'referer': 'https://www.myntra.com/sarees?f=Gender%3Amen%20women%2Cwomen&rf=Discount%20Range%3A10.0_100.0_10.0%20TO%20100.0',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    }

response = requests.get(
    'https://www.myntra.com/shirts'   , headers=headers,
)
html = response.text


start = html.find("window.__myx = ")

if start != -1:

    start = html.find("{", start)

    # Find the end before next script
    end = html.find("</script>", start)

    json_text = html[start:end].strip()

    # Remove trailing semicolon if present
    if json_text.endswith(";"):
        json_text = json_text[:-1]


    data = json.loads(json_text)


    products = data["searchData"]["results"]["products"]
    

#     for product in products :

#         print(product["productName"])

#         product_url = "https://www.myntra.com/" + product["landingPageUrl"]
#         print(product_url)

#         # images

#         images = []

#         for image in product["images"]:
#             images.append(image["src"])

#         # sku 
#         sku = product["buyButtonWinnerSkuId"]

#         gender = product["gender"]

        



##############################PARSER##############################
         
response = requests.get(
    # 'https://www.myntra.com/shirts/glitchez/glitchez-textured-slim-fit-casual-shirt/40842650/buy',
    'https://www.myntra.com/sarees/anouk/anouk-embellished-floral-sequinned-organza-saree/31819129/buy',
    
    headers=headers,
)

print(response.status_code)
html = response.text


start = html.find("window.__myx = ")

if start != -1:

    start = html.find("{", start)

    end = html.find("</script>", start)

    json_text = html[start:end].strip()

    if json_text.endswith(";"):
        json_text = json_text[:-1]

    data = json.loads(json_text)
    

    pdp = data["pdpData"]

    # print(pdp.keys())

    product_name = pdp["name"]
    MRPs =  pdp["mrp"]
    Manufacturer= pdp["manufacturer"]
    item_number= pdp["id"]

    price = pdp.get("price", {})


    discounted = price.get("discounted")

    price = discounted if discounted else  MRPs

    occasion = pdp["articleAttributes"].get("Occasions")

    for size in pdp.get("sizes", []):

       print("Size:", size["label"])
       print("SKU:", size["skuId"])
       print("Available:", size["available"])


    color = [colour["label"] for colour in pdp.get("colours", [])]

    selected_color = pdp["baseColour"]

    print(selected_color)

    sku = pdp["buyButtonSellerOrder"][0]["skuId"]

    print(sku)

    print(pdp.get("analytics",{}).get("subCategory") or "")
from bs4 import BeautifulSoup


soup = BeautifulSoup(html, "html.parser")

import json

breadcrumb = ""

for script in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(script.string)

        if data.get("@type") == "BreadcrumbList":
            breadcrumb = " > ".join(
                item["item"]["name"]
        
                for item in data["itemListElement"]
            )
            category = data["itemListElement"][0]["item"]["name"]

            break

    except Exception:
        continue

print(breadcrumb, category)


