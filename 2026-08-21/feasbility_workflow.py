import requests

import re

import json

##############################CRAWLER##############################

cookies = {
      'MCLVALID': ''
}

headers = {
    }

params = {
    'page': '1',
    'view': 'json',
}

response = requests.get('https://bevmo.com/collections/whiskies', params=params, cookies=cookies, headers=headers)



data =response.json()


total_pages = data.get('paginate', {}).get('pages')


product_ids = data.get('productIds', '')

product_ids = [int(x) for x in data.get('productIds', '').split(',')]

for page in range(1, total_pages + 1):

    print(f"Scraping page {page}/{total_pages}")

    params = {
        'page': page,
        'view': 'json',
    }

    response = requests.get(
        'https://bevmo.com/collections/whiskies',
        params=params,
        cookies=cookies,
        headers=headers
    )

    data = response.json()

    # Get product IDs and convert them to integers
    product_ids = [
        int(x.strip())
        for x in data.get('productIds', '').split(',')
        if x.strip()
    ]

    json_data = {
    'fulfillment_type': 'pickup',
    'selected_taxonomy': '',
    'location_id': 1,
    'filters': {},
    'sort_by': '',
    'per_page': 24,
    'adSessionId': '',
    'pageType': 'COLLECTION',
    'contentRequestId': '',
    'ids': [
        15719,
        3144,
        208523,
        67383,
        7569,
        8658,
        8656,
        12094,
        21550,
        12128,
        17257,
        12127,
        33976,
        12126,
        56043,
        11998,
        17377,
        12137,
        12135,
        71557,
        18568,
        15932,
        12138,
        33977,
    ],
    'sortOptions':[],
    'offset': 0,
    'shopify_shop_domain': 'bevmo-ca.myshopify.com',
    'unified': True,
}
    json_data['ids'] =  product_ids
    response = requests.post('https://bevmo.com/shopify/v1/bevmo/shops/products', cookies=cookies, headers=headers, json=json_data)
    data = response.json()

    datas = data.get('products','')

    for i in datas:
      product_name = i.get('title','')

      product_id = i.get('id','')

      images = i.get('image',{})

      tags = i.get('tags','')

      is_alcohol = i.get('is_alcohol','')

      is_tobacco = i.get('is_tobacco','')

      regular_price = i.get('price','')

      offer_price = i.get('offer','')


##############################PARSER##############################



cookies = {

        'MCLVALID': ''
       }

headers = {
    }



response = requests.get(f'https://bevmo.com/products/{product_id}', cookies=cookies, headers=headers)
from parsel import Selector

selector = Selector(text=response.text)

pdp_url =selector.xpath('//link[@rel="canonical"]/@href').get()


unique_id =  selector.xpath('//product-info/@data-gopuff-product-id').get()

product_name = selector.xpath('//meta[@property="og:title"]/@content').get()
# regular_price = selector.xpath('//meta[@property="og:price:amount"]/@content').get()

# product_schema = selector.xpath(  '//script[@id="ProductSchema"]/text()').get()

# product_data = json.loads(product_schema)

# offer_price  = product_data.get('offers', [{}])[0].get('price')

# offer_price = float(offer_price)

if float(regular_price) == offer_price:
    offer_price = ""
    selling_price = regular_price
else:
    selling_price = offer_price

currency = selector.xpath('//meta[@property="og:price:currency"]/@content').get()


Image = selector.xpath( '//div[contains(@class, "product-media-container")]//img/@src').getall()

product_description = selector.xpath('//meta[@name="description"]/@content').get()


warning = selector.xpath( '//p[contains(@class, "warning")]//text()').getall()

warning= ' '.join(text.strip() for text in warning if text.strip())


details = selector.xpath('//div[contains(@class, "product-details")]//li')

product_details = {}

for detail in details:
    label = detail.xpath(
        './/span[contains(@class, "product-details--list-label")]/text()'
    ).get()

    value = detail.xpath(
        './/span[contains(@class, "product-details--list-value")]/text()'
    ).get()

    if label and value:
        product_details[label.strip()] = value.strip()


size = product_details.get('Size', '')

alcohol_content = product_details.get('ABV', '')

country_of_origin = product_details.get('Country', '')

sku = product_details.get('SKU', '')


product_text = ' '.join(selector.xpath( '//p[contains(@class, "product__text")]//text()').getall()).strip()


match = re.search(r'([\d.]+)\s*([a-zA-Z]+)', product_text)

if match:
   
   grammage_quantity  = match.group(1)

   grammage_unit = match.group(2)

site_shown_uom = f"{grammage_quantity}{grammage_unit}"


special_information = selector.xpath( '//h4[contains(., "Government Issued ID Required for Purchase")]/following-sibling::p[1]/text()').get()


script = selector.xpath( '//script[contains(., "ShopifyAnalytics.lib.track")]/text()').get()


breadcrumbs = re.search(r'"category":"([^"]+)"', script).group(1)


brand = re.search(r'"brand":"([^"]+)"', script).group(1)



script_text = '\n'.join(selector.xpath('//script/text()').getall())

matchs = re.search(
    r'inventory_in_stock_show_count:\s*`([^`]*)`',
    script_text
)

if matchs:
     inventory_text = matchs.group(1)
     if "in stock" in inventory_text.lower():

          stock_availblity = "in_stock"
     else:
          stock_availblity = "out_of_stock"




