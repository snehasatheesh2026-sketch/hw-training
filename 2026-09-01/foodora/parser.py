
import logging
import requests
from datetime import datetime
from items import ProductdataItem
from settings import (
    API_URL,
    HEADERS,
    PRODUCT_JSON_DATA,
    client,
    MONGO_DB,
    MONGO_COLLECTION_DATA,
    MONGO_COLLECTION_PRODUCT_DATA,
)


class Parser:
    """Crawling Product Details"""

    def __init__(self):

        self.source_collection = client[ MONGO_DB][ MONGO_COLLECTION_DATA]

        self.product_collection = client[ MONGO_DB ][ MONGO_COLLECTION_PRODUCT_DATA]

        self.product_collection.create_index("unique_id", unique=True)

        self.session = requests.Session()

        self.session.headers.update(HEADERS)


    def start(self):

        products = self.source_collection.find({})

        for product in products:

            product_id = product.get("product_id")
            category = product.get("category", "")

            if not product_id:
                continue

            logging.info( "Product ID: %s | Category: %s", product_id, category )

            try:
                PRODUCT_JSON_DATA[
                    "variables"
                ][
                    "productIdentifier"
                ][
                    "value"
                ] = str(product_id)


                

                response = self.session.post(
                    API_URL,
                    headers=HEADERS,
                    json=PRODUCT_JSON_DATA,
                    timeout=30
                )


                logging.info( "Response status: %s", response.status_code)

                response.raise_for_status()


                self.parse_item( response, product_id,)


            except Exception:

                logging.exception(
                    "Failed product: %s",
                    product_id
                )


    def parse_item( self, response, product_id,):
        

        try:

            response_json = response.json()

        except ValueError:

            logging.exception(
                "Invalid JSON | Product ID: %s",
                product_id
            )

            return


        data = (response_json.get("data", {}).get("productDetails", {}).get("product", {}))


        if not data:
            logging.warning("No product data: %s",product_id )
            return


        # Initialize your fields

        netweight = ""
        country_of_origin = ""
        ingredients = ""
        storage_instructions = ""
        instructionforuse = ""
        size = ""
        special_information = ""
        currency = ""
        nutritional_information = ""
        product_name = ""
        product_decsription = ""
        product_unique_key = ""
        selling_price = ""
        regular_price = ""
        image_url_1 = ""
        image_url_2 =""
        image_url_3=""
        image_url_4=""
        image_url_5=""
        image_url_6=""
        extraction_date =""
        barcode = ""
        retail_limit = ""
        price_per_base_unit = ""
        gram_quantity = None
        gram_unit = ""
        site_shown_uom = ""

        unique_id = data.get("productID", product_id )

        product_unique_key = ( str(product_id) + "P")

        selling_price = data.get("price", "")

        regular_price = data.get("originalPrice", "")

        if not regular_price:

            regular_price = selling_price

        image_urls = data.get("urls", [])

        image_url_1, image_url_2, image_url_3, image_url_4, image_url_5, image_url_6 = (image_urls + [""] * 6 )[:6]

        product_name = data.get("name","")

        product_decsription = data.get("description","")

        product_infos = (data.get("foodLabelling", {}).get("productInfos",[]))

        attributes = data.get("attributes",[])


        if attributes:

            attrs = {
                item["key"]: item["value"]
                for item in attributes
                if item.get("key")
            }


            gram_unit = attrs.get( "contentsUnit", "")


            val = attrs.get("contentsValue","")


            try:

                gram_quantity = (float(val)if val else "")

            except (ValueError, TypeError):

                gram_quantity = ""


            if gram_quantity and gram_unit:

                site_shown_uom = f"{gram_quantity:g} {gram_unit}"


            retail_limit = attrs.get("maximumSalesQuantity","")


            barcode = attrs.get("pieceBarcodes","")


            unit_base = attrs.get("baseUnit","")


            price__base = attrs.get("pricePerBaseUnit", "")


            vaule_base = attrs.get("baseContentValue", "")


            if price__base and vaule_base:

                try:

                    price_per_base_unit = (
                        f"{float(price__base):.2f} "
                        f" je {vaule_base}"
                        f"{unit_base}"
                    )

                except (ValueError, TypeError):

                    price_per_base_unit = ""

        nutrition_facts = (data.get("foodLabelling",{}).get("nutritionFacts", [] ) or [] )

        nutritional_information = "; ".join(
            f"{x.get('labelTitle', '')}: "
            f"{x.get('labelValues', [''])[0]}"
            for x in nutrition_facts
            if x.get("labelValues")
        )

        extraction_date= datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        try:

            netweight = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Nettofüllmenge"

                    and x.get("labelValues")
                ),
                ""
            )


            country_of_origin = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Ursprungsland"

                    and x.get("labelValues")
                ),
                ""
            )


            ingredients = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    in [
                        "Zutaten "
                        "(Allergene hervorgehoben "
                        "in Großbuchstaben)",
                        "Zutaten"
                    ]

                    and x.get("labelValues")
                ),
                ""
            )


            storage_instructions = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Aufbewahrungshinweis"

                    and x.get("labelValues")
                ),
                ""
            )


            instructionforuse = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Verwendungshinweis"

                    and x.get("labelValues")
                ),
                ""
            )


            size = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Größe"

                    and x.get("labelValues")
                ),
                ""
            )


            special_information = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Weitere Informationen"

                    and x.get("labelValues")
                ),
                ""
            )


            currency = next(
                (
                    x.get(
                        "labelValues",
                        [""]
                    )[0]

                    for x in product_infos

                    if x.get("labelTitle")
                    == "Pfand (Währung)"

                    and x.get("labelValues")
                ),
                ""
            )


        except Exception:

            logging.exception(
                "Product info parsing failed: %s",
                unique_id
            )


        
        item ={
                            "unique_id":unique_id, 
                            "competitor_name": "foodora",
                            "store_name": "",
                            "store_addressline1": "",
                            "store_addressline2": "",
                            "store_suburb": "",
                            "store_state": "",
                            "store_postcode": "",
                            "store_addressid": "",
                            "extraction_date": extraction_date,
                            "product_name": product_name,
                            "brand": "",
                            "brand_type": "",
                            "grammage_quantity": gram_quantity,
                            "grammage_unit": gram_unit,
                            "drained_weight": "",
                            "producthierarchy_level1": "",
                            "producthierarchy_level2": "",
                            "producthierarchy_level3": "",
                            "producthierarchy_level4": "",
                            "producthierarchy_level5": "",
                            "producthierarchy_level6": "",
                            "regular_price": regular_price,
                            "selling_price": selling_price,
                            "price_was": "",
                            "promotion_price": "",
                            "promotion_valid_from": "",
                            "promotion_valid_upto": "",
                            "promotion_type": "",
                            "percentage_discount": "",
                            "promotion_description": "",
                            "package_sizeof_sellingprice": "",
                            "per_unit_sizedescription": "",
                            "price_valid_from": "",
                            "price_per_unit": price_per_base_unit,
                            "multi_buy_item_count": "",
                            "multi_buy_items_price_total": "",
                            "currency": currency,
                            "breadcrumb": "",
                            "pdp_url": "",
                            "variants": "",
                            "product_description": product_decsription,
                            "instructions": "",
                            "storage_instructions": storage_instructions,
                            "preparationinstructions": "",
                            "instructionforuse": instructionforuse,
                            "country_of_origin": country_of_origin,
                            "allergens": "",
                            "age_of_the_product": "",
                            "age_recommendations": "",
                            "flavour": "",
                            "nutritions": "",
                            "nutritional_information": nutritional_information,
                            "vitamins": "",
                            "labelling": "",
                            "grade": "",
                            "region": "",
                            "packaging": "",
                            "receipies": "",
                            "processed_food": "",
                            "barcode": barcode,
                            "frozen": "",
                            "chilled": "",
                            "organictype": "",
                            "cooking_part": "",
                            "Handmade": "",
                            "max_heating_temperature": "",
                            "special_information": special_information,
                            "label_information": "",
                            "dimensions": "",
                            "special_nutrition_purpose": "",
                            "feeding_recommendation": "",
                            "warranty": "",
                            "color": "",
                            "model_number": "",
                            "material": "",
                            "usp": "",
                            "dosage_recommendation": "",
                            "tasting_note": "",
                            "food_preservation": "",
                            "size": size,
                            "rating": "",
                            "review": "",
                            "file_name_1": "",
                            "image_url_1": image_url_1,
                            "file_name_2": "",
                            "image_url_2": image_url_2,
                            "file_name_3": "",
                            "image_url_3": image_url_3,
                            "file_name_4": "",
                            "image_url_4": image_url_4,
                            "file_name_5": "",
                            "image_url_5": image_url_5,
                            "file_name_6": "",
                            "image_url_6": image_url_6,
                            "competitor_product_key": "",
                            "fit_guide": "",
                            "occasion": "",
                            "material_composition": "",
                            "style": "",
                            "care_instructions": "",
                            "heel_type": "",
                            "heel_height": "",
                            "upc": "",
                            "features": "",
                            "dietary_lifestyle": "",
                            "manufacturer_address": "",
                            "importer_address": "",
                            "distributor_address": "",
                            "vinification_details": "",
                            "recycling_information": "",
                            "return_address": "",
                            "alchol_by_volume": "",
                            "beer_deg": "",
                            "netcontent": "",
                            "netweight": netweight,
                            "site_shown_uom": site_shown_uom,
                            "ingredients": ingredients,
                            "random_weight_flag": "",
                            "instock": "",
                            "promo_limit": "",
                            "product_unique_key": product_unique_key,
                            "multibuy_items_pricesingle": "",
                            "perfect_match": "",
                            "servings_per_pack": "",
                            "Warning": "",
                            "suitable_for": "",
                            "standard_drinks": "",
                            "environmental": "",
                            "grape_variety": "",
                            "retail_limit": retail_limit,
                        }

 


        try:

            product = ProductdataItem(**item)
            product.save()
            



            logging.info(
                "Product saved: %s",
                product_id
            )


        except Exception:

            logging.exception(
                "Mongo save failed: %s",
                product_id
            )


    def close(self):

        self.session.close()


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s"
    )


    crawler = Parser()

    try:

        crawler.start()

    finally:

        crawler.close()