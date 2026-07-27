import requests
from parsel import Selector

import re
from urllib.parse import urljoin

import json

##############################CRAWLER##############################
cookies = {
         }

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-IN,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
}

response = requests.get('https://www.webstaurantstore.com/25887/commercial-gas-ranges.html',cookies=cookies,headers=headers,)
selectors = Selector(text= response.text)


product_list = selectors.xpath('//div[@data-testid="productBoxContainer"]')
base_url = 'https://www.webstaurantstore.com/'
for product in product_list:
    rel_url = product.xpath('.//a[@data-testid="itemLink"]/@href | .//a/@href').get()
    if not rel_url:
         continue

    product_url = urljoin(base_url, rel_url)


##############################PARSER##############################
response = requests.get(
    'https://www.webstaurantstore.com/cooking-performance-group-s24-n-natural-gas-4-burner-24-range-with-standard-oven-150-000-btu/351S24N.html',
    cookies=cookies,
    headers=headers,
)

Selected_Variant = {}
configurable_attributes = []

selector = Selector(text =response.text)

product_name = selector.xpath('normalize-space(//h1[@data-testid="product-detail-heading"])').get() or ""



raw_rating = selector.xpath('//span[@data-testid="zest-ratings-sr"]/text()').get() or ""
match = re.search(r'(\d+(?:\.\d+)?)', raw_rating)
rating = match.group(1) if match else ""



documents = [ url for url in selector.xpath('//div[@id="resources-group"]//a/@href' ).getall() if url.lower().endswith((
".pdf",".doc",".docx",".xls" ".xlsx", ".ppt",".pptx",".zip" )) ]


brand = selector.xpath('normalize-space(//*[@data-testid="brand-side-section"]//a/@title)').get() or ""



video = selector.xpath('//source[contains(@src, "_4.mp4")]/@src').get("")



for heading in selector.xpath( '//h2[@data-testid="productVariationsHeading"]'):
    s_name = heading.xpath( 'normalize-space(text())').get("").replace(":", "").strip()

    s_value = heading.xpath('./span/text()').get("").strip()

    if s_name and s_value:
        Selected_Variant[s_name] = s_value

        if s_name not in configurable_attributes:
            configurable_attributes.append(s_name)

if not Selected_Variant:
                    Selected_Variant = ""

configurable_attributes = (",".join(configurable_attributes) if configurable_attributes else "")

product_overview = selector.xpath('//h3[normalize-space()="Product Overview"]'
                                  '/following-sibling::ul[1]/li/span/text()').getall()


product_overview = [ x.strip()for x in product_overview if x.strip()]

Features = ",".join(product_overview) if product_overview else ""


price_container = (selector.xpath('//*[@data-testid="price-container"]') or selector.xpath('//div[contains(@class,"map__price")]'))
                
if price_container:
    full_price_text = " ".join(t.strip() for t in price_container.xpath(".//text()").getall() if t.strip()
                                            )
    price_match = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", full_price_text)
                
    if price_match:
                
                
        price = price_match.group(1).replace(",", "")
    unit_match = re.search(r"/\s*([A-Za-z0-9 .-]+)", full_price_text)

    if unit_match:
        price_unit = unit_match.group(1).strip()


# ---------------- Shipping ----------------
shipping_info = selector.xpath('normalize-space(.//*[@data-testid="highlights-meta-side-section"]//p)').get() or ""



upc = str(selector.xpath('normalize-space(.//*[@data-testid="UPC-Number"])').get() or "")

Specifications = {key.strip(): " ".join(value.xpath(".//text()").getall()).strip()
                    for key, value in zip(
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dt/text()').getall(),
                        selector.xpath('//dl[@id="tbSpecSheetRows"]/dd'))}

related_product_skus =str (",".join(
                    s.split("relatedproduct_companion_")[-1]
                    for s in selector.xpath(
                    '//div[contains(@class,"add-to-cart")]//form[starts-with(@id,"relatedproduct_companion_")]/@id'
                    ).getall()))

# descrpition 
intro_container = selector.xpath(
                    '//*[@data-testid="introduction"]'
                )

if intro_container:
    intro_headline = intro_container.xpath(
                        'normalize-space(.//*[@id="details-group-headline"] | .//h2)' ).get() or ""

    description = intro_container.xpath(
    'string(.//div[contains(@class,"template-text")] | .//p)' ).get() or ""

if not description:
    details_group = selector.xpath(
                        '//*[@data-testid="details-group"]' )

    if details_group:
        escription = details_group.xpath(
                            'string(.//div[@class="padded"])').get() or ""

descrpition  = f"{intro_headline} {description}".strip()


for faq in selector.xpath("//div[contains(@class,'customer-qa')]"):
                    question = faq.xpath(
                            "normalize-space(.//div[contains(@class,'customer-question')])"
                              ).get(default="")
                    answer = " ".join(t.strip() for t in faq.xpath(".//div[contains(@class,'csr-answer')]//text()").getall()if t.strip())
                    
product = {}
for script in selector.xpath('//script/text()').getall():
    if "productTemplates" in script:
        try:
            script = script.strip()
            script = script.removeprefix("<!--").removesuffix("-->").strip()
            data = json.loads(script)
            product = data["productTemplates"][0]
            sku = str(product.get("itemNumberId", ""))
            break
        except Exception:
               pass


image_urls=[]     
for href in selector.xpath('//div[@data-testid="main-slider-item"]//img/@src').getall():

      if f"/products/large/{sku}/" in href:
                match = re.search(r'(images/products/large/.*)', href)
                if match:
                   image_urls.append(match.group(1))
      
image_urls = list(dict.fromkeys(image_urls))

model_list = []
for script in selector.xpath(
                    '//script[@type="application/ld+json"]/text()'
).getall():

            try:
               data = json.loads(script.strip())
               nodes = data if isinstance(data, list) else data.get("@graph", [data])
               for node in nodes:
                    if isinstance(node, dict) and node.get("@type") == "3DModel":
                        for obj in node.get("encoding", []):
                           url = obj.get("contentUrl")
                           if url:
                                model_list.append(url.lstrip("/"))
            except json.JSONDecodeError:
                     continue

variants = {}
for group in product.get("variationMembership", {}).get("variationGroups", []):
    attr = group.get("optionName", "")
    if attr == "Height Style":
        attr = "Height"
    for item_var in group.get("variationGroupItems", []):
        skus = str(item_var.get("itemNumberId", ""))
        if not skus:
            continue
        variants.setdefault(skus, {"sku": skus})
        variants[skus][attr] = item_var.get("variationText", "")
        Configurable_Variations = list(variants.values()) if variants else ""


page_breadcrumbs = ""
bc_script = selector.xpath('//script[contains(text(),"BreadcrumbList")]/text()').get()
if bc_script:
        try:
           data = json.loads(bc_script.strip())
           nodes = data if isinstance(data, list) else data.get("@graph", [data])
           for node in nodes:
                if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":
                    crumbs = [cb.get("name")for cb in node.get("itemListElement", [])if cb.get("name")]
                    if crumbs:
                        page_breadcrumbs = " > ".join(crumbs[:-1])
                        break
        except Exception:
             pass
print(page_breadcrumbs)
    
