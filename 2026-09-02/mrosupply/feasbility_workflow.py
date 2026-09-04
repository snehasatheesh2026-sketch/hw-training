import requests
from urllib.parse import urljoin
from parsel import Selector
import json



##############################CRAWLER##############################


base_url = "https://www.mrosupply.com/"
headers = {
      }

params = {
    'page':'1' ,}

response = requests.get(
        'https://www.mrosupply.com/electric-motors/ac-motors/',
        params=params,
        headers=headers,
        timeout=10
    )

selector = Selector(response.text)

products = selector.xpath('//div[contains(@class,"m-catalogue-product")]'
        '//a[contains(@class,"js-product-link")]/@href'
    ).getall()



for url in products:
        pdp_url = urljoin(base_url,url)

##############################PARSER##############################

headers = {
    }

response = requests.get(pdp_url, headers=headers)

selector = Selector(response.text)

item_name = selector.xpath('//meta[@name="twitter:title"]/@value').get()

price = selector.xpath('//meta[@name="twitter:data3"]/@value').get()

uoi = selector.xpath('//p[@title="UNIT OF MEASURE"]/../../div[2]//p/text()').get()

qty = selector.xpath('//input[@name="qty"]/@value').get()

brand = selector.xpath('//a[contains(@class,"js-brand-name")]/text()').get()

vendor_seller_part_number = selector.xpath('//div[contains(@class,"flex-table--head")]/p[normalize-space()="SKU"]/../following-sibling::div[contains(@class,"flex-table--body")]/p/text()').get()

unique_id = vendor_seller_part_number

model_number= selector.xpath('//p[contains(@class,"modelNo")]/text()[normalize-space()]').get()

pdp_url = selector.xpath('//link[@rel="canonical"]/@href').get()

lead_time= selector.xpath('//p[contains(@class,"muted") and contains(.,"Typically Ships in")]/span/text()').get()

data = selector.xpath('//script[@type="application/ld+json"]/text()').get()

json_data = json.loads(data)

availability = json_data[0]["offers"][0]["availability"].split("/")[-1]

company_name = json_data[0]["offers"][0]["seller"]["name"]

category = selector.xpath('//meta[@name="twitter:label2" and @value="Category"]/following-sibling::meta[@name="twitter:data2"]/@value').get()

description = selector.xpath('//meta[@name="description"]/@content').get()

description = selector.xpath('//div[@id="accordion-additionalDescription"]//div[contains(@class,"m-accordion--item--body")]').xpath('string(.)').get()

manufacturer_part_number = model_number


Additional_info = []

for item in selector.xpath(
    "//div[@id='accordion-attributes']//div[contains(@class,'o-grid-item')]"
):
    key = item.xpath("normalize-space(.//p[@class='key'])").get()
    value = item.xpath("normalize-space(.//p[@class='value'])").get()

    Additional_info.append(f"{key}: {value}")
