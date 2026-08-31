import logging
import requests
import re
import json
from parsel import Selector
from items import ProductdataItem
from settings import (
    HEADERS,
    COOKIES,
    MONGO_COLLECTION_DATA,
    MONGO_COLLECTION_PRODUCT_DATA,
    client,
    MONGO_DB
)


class Parser:

    def __init__(self):
        self.db = client[MONGO_DB]
        self.source_collection = self.db[MONGO_COLLECTION_DATA]
        self.data_collection = self.db[MONGO_COLLECTION_PRODUCT_DATA]
        self.data_collection.create_index( "product_url",unique=True)
        
        
    def start(self):

        metas = self.source_collection.find({})
        
        for meta in metas:
            url = meta.get('product_url')

            if not url:
                continue
            try:
                response = requests.get(url, headers=HEADERS, cookies=COOKIES, timeout=30)
                if response and response.status_code == 200:
                    self.parse_item(url, response, meta)

                else:
                    logging.warning(f"Failed to fetch {url}, status code: {response.status_code if response else 'No Response'}")
                
            except Exception as e:
                logging.error(f"Error requesting {url}: {e}")

    def close(self):
        
        self.mongo.close()
        

    def parse_item(self, url, response, meta):
        """item part"""
        Selected_Variant = {}
        configurable_attributes = []
        faqs = []
        seen = set()
        product = {}
        sku = ""
        image_urls = []
        variants = {}
        model_list = []
        page_breadcrumbs = ""


        sel = Selector(text=response.text)

        # XPATH
        PRODUCT_NAME_XPATH = '//h1[@data-testid="product-detail-heading"]/text()'
        DOCUMENT_XPATH =  '//div[@id="resources-group"]//a/@href'
        VIDEO_XPATH =  '//source[contains(@src, "_4.mp4")]/@src'
        VARIANT_HEADING_XPATH = '//h2[@data-testid="productVariationsHeading"]'
        PRODUCT_OVERVIEW_XPATH = ('//h3[normalize-space()="Product Overview"]'
                                  '/following-sibling::ul[1]/li/span/text()')
        RATING_XPATH = '//span[@data-testid="zest-ratings-sr"]/text()'
        PRICE_CONTAINER_XPATH = ('//*[@data-testid="price-container"] | '
                                 '//div[contains(@class,"map__price")]')
        BRAND_XPATH = 'normalize-space(//*[@data-testid="brand-side-section"]//a/@title)'
        INTRO_CONTAINER_XPATH = '//*[@data-testid="introduction"]'
        INTRO_HEADLINE_XPATH = 'normalize-space(.//*[@id="details-group-headline"] | .//h2)'
        DESCRIPTION_XPATH = 'string(.//div[contains(@class,"template-text")] | .//p)'
        DETAILS_GROUP_XPATH = '//*[@data-testid="details-group"]'
        DETAILS_DESCRIPTION_XPATH = 'string(.//div[@class="padded"])'
        SHIPPING_INFO_XPATH = 'normalize-space(.//*[@data-testid="highlights-meta-side-section"]//p)'
        UPC_XPATH = 'normalize-space(.//*[@data-testid="UPC-Number"])'
        SPECIFICATION_KEY_XPATH = '//dl[@id="tbSpecSheetRows"]/dt/text()'
        SPECIFICATION_VALUE_XPATH = '//dl[@id="tbSpecSheetRows"]/dd'
        RELATED_PRODUCT_SKUS_XPATH = ('//div[contains(@class,"add-to-cart")]'
                                      '//form[starts-with(@id,"relatedproduct_companion_")]/@id')
        FAQ_XPATH = "//div[contains(@class,'customer-qa')]"
        QUESTION_XPATH = "normalize-space(.//div[contains(@class,'customer-question')])"
        ANSWER_XPATH = ".//div[contains(@class,'csr-answer')]//text()"
    
        PRODUCT_SCRIPT_XPATH = '//script/text()'
        IMAGE_XPATH = '//div[@data-testid="main-slider-item"]//img/@src'
        MODEL_JSON_XPATH = '//script[@type="application/ld+json"]/text()'
        BREADCRUMB_XPATH = '//script[contains(text(),"BreadcrumbList")]/text()'



        # EXTRACT
        product_name = sel.xpath(PRODUCT_NAME_XPATH).get()
        print(product_name)
        documents = [url for url in sel.xpath(DOCUMENT_XPATH).getall() if url.lower().endswith((".pdf",".doc",".docx", ".xls", ".xlsx", ".ppt",".pptx",".zip"))]
        documents = list(dict.fromkeys(documents))
        video = sel.xpath(VIDEO_XPATH).get(default="")
        for heading in sel.xpath(VARIANT_HEADING_XPATH):
                s_name = heading.xpath('normalize-space(text())').get("").replace(":", "").strip()
        
                s_value = heading.xpath('./span/text()').get("").strip()
        
                if s_name and s_value:
                    Selected_Variant[s_name] = s_value
        
                    if s_name not in configurable_attributes:
                            configurable_attributes.append(s_name)
        product_overview = sel.xpath(PRODUCT_OVERVIEW_XPATH).getall()
        raw_rating = sel.xpath(RATING_XPATH).get(default="")
        matchs = re.search(r'(\d+(?:\.\d+)?)', raw_rating)
        price_container = sel.xpath(PRICE_CONTAINER_XPATH)
        full_price_text = " ".join( x.strip() for x in price_container.xpath(".//text()").getall() if x.strip())
        brand =sel.xpath (BRAND_XPATH).get(default="")
        intro_container = sel.xpath(INTRO_CONTAINER_XPATH)

        intro_headline = intro_container.xpath(INTRO_HEADLINE_XPATH).get(default="") if intro_container else ""
        description = intro_container.xpath(DESCRIPTION_XPATH).get(default="") if intro_container else ""

        if not description:
            details_group = sel.xpath(DETAILS_GROUP_XPATH)
            description = details_group.xpath(DETAILS_DESCRIPTION_XPATH).get(default="") if details_group else ""
        shipping_info = sel.xpath(SHIPPING_INFO_XPATH).get(default="")
        upc = sel.xpath(UPC_XPATH).get(default="")
        specification_keys = sel.xpath(SPECIFICATION_KEY_XPATH).getall()
        specification_values = sel.xpath(SPECIFICATION_VALUE_XPATH)
        related_product_skus = sel.xpath(RELATED_PRODUCT_SKUS_XPATH).getall()
        for faq in sel.xpath(FAQ_XPATH):
           question = faq.xpath(QUESTION_XPATH).get(default="")
           answer = " ".join(x.strip() for x in faq.xpath(ANSWER_XPATH).getall() if x.strip())
           if question and answer:
               key = (question, answer)
               if key not in seen:
                     seen.add(key)
                     faqs.append({ "Question": question,"Answer": answer})
        for script in sel.xpath(PRODUCT_SCRIPT_XPATH).getall():
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
        if sku:
           for href in sel.xpath(IMAGE_XPATH).getall():
              if f"/products/large/{sku}/" in href:
                 match = re.search(r"(images/products/large/.*)", href)
                 if match:
                   image_urls.append(match.group(1))
        for group in product.get("variationMembership", {}).get("variationGroups", []):
            attr = group.get("optionName", "")
            if attr == "Height Style":
                attr = "Height"
            for item_var in group.get("variationGroupItems", []):
                  variant_sku = str(item_var.get("itemNumberId", ""))

                  if not variant_sku:
                    continue

                  variants.setdefault(variant_sku, {"sku": variant_sku})
                  variants[variant_sku][attr] = item_var.get("variationText", "")
        for script in sel.xpath(MODEL_JSON_XPATH).getall():
            try:
               data = json.loads(script.strip())

               nodes = data if isinstance(data, list) else data.get("@graph", [data])

               for node in nodes:
                 if isinstance(node, dict) and node.get("@type") == "3DModel":
                   for obj in node.get("encoding", []):
                       urls= obj.get("contentUrl")

                       if urls:
                           model_list.append(urls.lstrip("/"))

            except json.JSONDecodeError:
              continue
        bc_script = sel.xpath(BREADCRUMB_XPATH).get()

        if bc_script:
            try:
              data = json.loads(bc_script.strip())

              nodes = data if isinstance(data, list) else data.get("@graph", [data])

              for node in nodes:
                if isinstance(node, dict) and node.get("@type") == "BreadcrumbList":

                    crumbs = [
                    cb.get("name")
                    for cb in node.get("itemListElement", [])
                    if cb.get("name")
                    ]
                    if crumbs:
                       page_breadcrumbs = " > ".join(crumbs[:-1])
                       break

            except Exception:
                 pass

       # CLEAN
        product_name = product_name.strip() if product_name else ""
        product_documents = ",".join(documents) if documents else ""
        video = video if video else ""
        Selected_Variant = Selected_Variant if Selected_Variant else ""
        configurable_attributes = (",".join(configurable_attributes)if configurable_attributes else "")
        Features = ", ".join(x.strip() for x in product_overview if x.strip())
        rating = matchs.group(1) if matchs else ""
        price_match = re.search(r"\$?\s*([\d,]+(?:\.\d+)?)", full_price_text)
        price = price_match.group(1).replace(",", "") if price_match else ""
        unit_match = re.search(r"/\s*([A-Za-z0-9 .-]+)", full_price_text)
        price_unit = unit_match.group(1).strip() if unit_match else ""
        intro_headline = intro_headline.strip()
        description = description.strip()
        product_details = f"{intro_headline} {description}".strip()
        Specifications = { key.strip(): " ".join(value.xpath(".//text()").getall()).strip()
                          for key, value in zip(specification_keys, specification_values)} or ""
        related_product_skus = ",".join(sku.split("relatedproduct_companion_")[-1] for sku in related_product_skus)
        faq_json = json.dumps(faqs,ensure_ascii=False,separators=(",", ":")) if faqs else ""
        image_urls = list(dict.fromkeys(image_urls))
        Product_Image_URLs = ",".join(image_urls) if image_urls else ""
        result = list(variants.values()) if variants else ""
        models = ",".join(model_list) if model_list else ""

        

        # ITEM BUILD
        item = {}
        item['product_url'] = url
        item['name'] = product_name
        item['brand'] = brand
        item['sku'] = sku
        item['rating'] = rating
        item['shipping_info'] = shipping_info
        item['upc'] = upc
        item['documnet'] = product_documents
        item['category'] = meta.get('category_name', '')
        if meta.get('item_number'):
            item['item_number'] = meta.get('item_number')
        item['video'] = video
        item['price'] = price
        item['price_unit'] = price_unit
        item['product_details'] = product_details
        item['features'] = Features
        item['selected_variant'] = Selected_Variant
        item['configurable_attributes'] = configurable_attributes
        item['specifications'] = Specifications
        item['related_product_skus'] = related_product_skus
        item['faq'] = faq_json
        item['images'] = Product_Image_URLs
        item['Configurable Variations'] = result
        item['m_3Dmodel'] = models
        item['breadcrumbs'] =  page_breadcrumbs


        logging.info(item)
        try:
            
            product_item = ProductdataItem(**item)

            product_item.save()
        except Exception as e:
            logging.error(f"Error saving product data to MongoDB: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser_obj = Parser()
    parser_obj.start()
    parser_obj.close()