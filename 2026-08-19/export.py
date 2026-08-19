

import csv
import logging
import json
from settings import (
    MONGO_COLLECTION_PRODUCT_DATA,
    file_name,
    FILE_HEADERS,
    client,
    MONGO_DB
)
seen_urls = set()

class Export:
    """Export MongoDB data to CSV"""

    def __init__(self, writer):
        self.writer = writer
        self.db = client[MONGO_DB]

    def start(self):

        self.writer.writerow(FILE_HEADERS)

        for item in self.db[MONGO_COLLECTION_PRODUCT_DATA].find(
            no_cursor_timeout=True
        ):
             url = item.get("unique_id", "")
             if url in seen_urls:
               print(f"Duplicate URL skipped: {url}")
               continue
             seen_urls.add(url)
             unique_id = item.get('unique_id','')

             print(unique_id)
             competitor_name = item.get('competitor_name','')
             store_name = item.get('store_name','')
             store_addressline1 = item.get('store_addressline1','')
             store_addressline2 = item.get('store_addressline2','')
             store_suburb = item.get('store_suburb','')
             store_state = item.get('store_state','')
             store_postcode = item.get('store_postcode','')
             store_addressid = item.get('store_addressid','')
             extraction_date = item.get('extraction_date','')
             product_name = item.get('product_name','')
             brand = item.get('brand','')
             brand_type = item.get('brand_type','')
             grammage_quantity = item.get('grammage_quantity','')
             grammage_unit = item.get('grammage_unit','')
             drained_weight = item.get('drained_weight','')
             producthierarchy_level1 = item.get('producthierarchy_level1','')
             producthierarchy_level2 = item.get('producthierarchy_level2','')
             producthierarchy_level3 = item.get('producthierarchy_level3','')
             producthierarchy_level4 = item.get('producthierarchy_level1','')
             regular_price = item.get('regular_price','')
             selling_price = item.get('selling_price','')
             price_was = item.get('price_was','')
             promotion_price = item.get('promotion_price','')
             promotion_valid_from = item.get('promotion_valid_from','')
             promotion_valid_upto = item.get('promotion_valid_upto','')
             promotion_type = item.get('promotion_type','')
             percentage_discount = item.get('percentage_discount','')
             promotion_description = item.get('promotion_description','')
             package_sizeof_sellingprice = item.get('package_sizeof_sellingprice','')
             per_unit_sizedescription = item.get('per_unit_sizedescription','')
             price_valid_from = item.get('price_valid_from','')
             price_per_unit = item.get('price_per_unit','')
             multi_buy_item_count = item.get('multi_buy_item_count','')
             multi_buy_items_price_total = item.get('multi_buy_items_price_total','')
             currency = item.get('currency','')
             breadcrumb = item.get('breadcrumb','')
             pdp_url = item.get('pdp_url','')
             variants = item.get('variants','')
             product_description = item.get('product_description','')
             instructions = item.get('instructions','')
             storage_instructions = item.get('storage_instructions','')
             preparationinstructions = item.get('preparationinstructions','')
             instructionforuse =  item.get('instructionforuse','')
             country_of_origin = item.get('country_of_origin','')
             allergens = item.get('allergens','')
             age_of_the_product = item.get('age_of_the_product','')
             age_recommendations = item.get('age_recommendations','')
             flavour = item.get('flavour','')
             nutritions = item.get('nutritions','')
             nutritional_information = item.get('nutritional_information','')
             vitamins = item.get('vitamins','')
             labelling = item.get('labelling','')
             grade = item.get('grade','')
             region = item.get('region','')
             packaging = item.get('packaging','')
             receipies = item.get('receipies','')
             processed_food = item.get('processed_food','')
             barcode = item.get('barcode','')
             frozen = item.get('frozen','')
             chilled = item.get('chilled','')
             organictype = item.get('organictype','')
             cooking_part = item.get('cooking_part','')
             Handmade = item.get('Handmade','')
             max_heating_temperature = item.get('max_heating_temperature','')
             special_information = item.get('special_information','')
             label_information = item.get('label_information','')
             dimensions = item.get('dimensions','')
             special_nutrition_purpose = item.get('special_nutrition_purpose','')
             feeding_recommendation = item.get('feeding_recommendation','')
             warranty = item.get('warranty','')
             color = item.get('color','')
             model_number= item.get('model_number','')
             material = item.get('material','')
             usp = item.get('usp','')
             dosage_recommendation = item.get('dosage_recommendation','')
             tasting_note = item.get('tasting_note','')
             food_preservation = item.get('food_preservation','')
             size = item.get('size','')
             rating = item.get('rating','')
             review = item.get('review','')
             file_name_1 = item.get('file_name_1','')
             image_url_1 = item.get('image_url_1','')
             file_name_2 = item.get('file_name_2','')
             image_url_2 = item.get('image_url_2','')
             file_name_3 = item.get('file_name_3','')
             image_url_3 = item.get('image_url_3','')
             file_name_4 = item.get('file_name_4','')
             image_url_4 = item.get('image_url_4','')
             file_name_5 = item.get('file_name_5','')
             image_url_5 = item.get('image_url_5','')
             file_name_6 = item.get('file_name_6','')
             image_url_6 = item.get('image_url_6','')
             competitor_product_key = item.get('competitor_product_key','')
             fit_guide= item.get('fit_guide','')
             occasion  = item.get('occasion','')
             material_composition= item.get('material_composition','')
             style = item.get('style','')
             care_instructions = item.get('care_instructions','')
             heel_type = item.get('heel_type','')
             heel_height = item.get('heel_height','')
             upc = item.get('upc','')
             features = item.get('features','')
             dietary_lifestyle = item.get('dietary_lifestyle','')
             manufacturer_address = item.get('manufacturer_address','')
             importer_address = item.get('importer_address','')
             distributor_address = item.get('distributor_address','')
             vinification_details = item.get('vinification_details','')
             recycling_information = item.get('recycling_information','')
             return_address = item.get('return_address','')
             alchol_by_volume = item.get('alchol_by_volume','')
             beer_deg = item.get('beer_deg','')
             netcontent = item.get('netcontent','')
             netweight = item.get('netweight','')
             site_shown_uom = item.get('site_shown_uom','')
             ingredients = item.get('ingredients','')
             random_weight_flag = item.get('random_weight_flag','')
             instock = item.get('instock','')
             promo_limit = item.get('promo_limit','')
             product_unique_key = item.get('product_unique_key','')
             multibuy_items_pricesingle = item.get('multibuy_items_pricesingle','')
             perfect_match = item.get('perfect_match','')
             servings_per_pack = item.get('servings_per_pack','')
             Warning = item.get('Warning','')
             suitable_for = item.get('suitable_for','')
             standard_drinks = item.get('standard_drinks','')
             environmental = item.get('environmental','')
             grape_variety = item.get('grape_variety','')
             retail_limit = item.get('retail_limit','')

             product_description = product_description.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace(';','').replace('::','').strip()

             ingredients = ingredients.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace('-',' ').replace(';','').replace('::','').strip()

             special_information = special_information.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace(';','').replace('::','').strip()

             product_name = product_name.replace('.','').strip()
             nutritional_information = nutritional_information.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace(';','').replace('::','').strip()

             storage_instructions = storage_instructions.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace(';','').replace('::','').strip()

             instructionforuse = instructionforuse.replace('\n','').replace('*','').replace('**','').replace('/',"_").replace('(',' ').replace(')','').replace('#','').replace('@','').replace('[',' ').replace(']','').replace(';','').replace('::','').strip()

             price_per_unit = " ".join(price_per_unit.split())

             if barcode:
                 barcode = str(barcode).split(",")[0].strip()

             if grammage_quantity in (0, 0.0, "0", "0.0"):
                 grammage_quantity = ""

             if selling_price != "":
                   selling_price = f"{selling_price:.2f}"

             if regular_price != "":
                  regular_price = f"{regular_price:.2f}"
            #  if currency == "":
            #      currency ="EUR"


             data = [
    unique_id,
    competitor_name,
    store_name,
    store_addressline1,
    store_addressline2,
    store_suburb,
    store_state,
    store_postcode,
    store_addressid,
    extraction_date,
    product_name,
    brand,
    brand_type,
    grammage_quantity,
    grammage_unit,
    drained_weight,
    producthierarchy_level1,
    producthierarchy_level2,
    producthierarchy_level3,
    producthierarchy_level4,
    regular_price,
    selling_price,
    price_was,
    promotion_price,
    promotion_valid_from,
    promotion_valid_upto,
    promotion_type,
    percentage_discount,
    promotion_description,
    package_sizeof_sellingprice,
    per_unit_sizedescription,
    price_valid_from,
    price_per_unit,
    multi_buy_item_count,
    multi_buy_items_price_total,
    currency,
    breadcrumb,
    pdp_url,
    variants,
    product_description,
    instructions,
    storage_instructions,
    preparationinstructions,
    instructionforuse,
    country_of_origin,
    allergens,
    age_of_the_product,
    age_recommendations,
    flavour,
    nutritions,
    nutritional_information,
    vitamins,
    labelling,
    grade,
    region,
    packaging,
    receipies,
    processed_food,
    barcode,
    frozen,
    chilled,
    organictype,
    cooking_part,
    Handmade,
    max_heating_temperature,
    special_information,
    label_information,
    dimensions,
    special_nutrition_purpose,
    feeding_recommendation,
    warranty,
    color,
    model_number,
    material,
    usp,
    dosage_recommendation,
    tasting_note,
    food_preservation,
    size,
    rating,
    review,
    file_name_1,
    image_url_1,
    file_name_2,
    image_url_2,
    file_name_3,
    image_url_3,
    file_name_4,
    image_url_4,
    file_name_5,
    image_url_5,
    file_name_6,
    image_url_6,
    competitor_product_key,
    fit_guide,
    occasion,
    material_composition,
    style,
    care_instructions,
    heel_type,
    heel_height,
    upc,
    features,
    dietary_lifestyle,
    manufacturer_address,
    importer_address,
    distributor_address,
    vinification_details,
    recycling_information,
    return_address,
    alchol_by_volume,
    beer_deg,
    netcontent,
    netweight,
    site_shown_uom,
    ingredients,
    random_weight_flag,
    instock,
    promo_limit,
    product_unique_key,
    multibuy_items_pricesingle,
    perfect_match,
    servings_per_pack,
    Warning,
    suitable_for,
    standard_drinks,
    environmental,
    grape_variety,
    retail_limit,
]








            

             self.writer.writerow(data)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    with open(file_name, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        export = Export(writer)
        export.start()

    print("CSV Export Completed")