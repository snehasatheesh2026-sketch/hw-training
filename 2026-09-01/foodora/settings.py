from datetime import datetime
import calendar
import logging
import pytz
from pymongo import MongoClient
from mongoengine import connect

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# basic details
PROJECT = "foodora"
CLIENT_NAME = ""
PROJECT_NAME = "foodora"
FREQUENCY = "ONETIME"
API_URL= "https://mj.fd-api.com/api/v5/graphql"

datetime_obj = datetime.now(pytz.timezone("Asia/Kolkata"))

iteration = datetime_obj.strftime("%Y_%m_%d")
YEAR = datetime_obj.strftime("%Y")
MONTH = datetime_obj.strftime("%m")
DAY = datetime_obj.strftime("%d")
MONTH_VALUE = calendar.month_abbr[int(MONTH.lstrip("0"))]
WEEK = (int(DAY) - 1) // 7 + 1

FILE_NAME = f"fDataHut_Foodora_{iteration}.csv"

# Mongo db and collections
MONGO_DB = f"foodora_{iteration}"
MONGO_COLLECTION_RESPONSE = f"{PROJECT_NAME}_url"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_DATA = f"{PROJECT_NAME}_data"
MONGO_COLLECTION_PRODUCT_DATA =  f"{PROJECT_NAME}__PRODUCT_data"



JSON_DATA = {}


HEADERS = {
        }




client = MongoClient("mongodb://localhost:27017/")



MAIN_CATEGORIES =  [
    "Obst & Gemüse",
    "Fisch",
    "Nahrungsmittel",
    "Tiefkühl",
    "Günstig grillen & genießen",
    "Frisch aus dem Ofen",
    "Brot & Gebäck",
    "Food For Future (vegan)",
    "Fleisch & Wurst",
    "Best of PENNY",
    "Kühlregal",
    "Süßes & Salziges",
    "Getränke & Co",
    "Convenience",
    "PENNY Ready"
]



CATEGORY_JSON_DATA = {
    }


PRODUCT_JSON_DATA = {}
FILE_HEADERS = [
    "unique_id",
    "competitor_name",
    "store_name",
    "store_addressline1",
    "store_addressline2",
    "store_suburb",
    "store_state",
    "store_postcode",
    "store_addressid",
    "extraction_date",
    "product_name",
    "brand",
    "brand_type",
    "grammage_quantity",
    "grammage_unit",
    "drained_weight",
    "producthierarchy_level1",
    "producthierarchy_level2",
    "producthierarchy_level3",
    "producthierarchy_level4",
    "regular_price",
    "selling_price",
    "price_was",
    "promotion_price",
    "promotion_valid_from",
    "promotion_valid_upto",
    "promotion_type",
    "percentage_discount",
    "promotion_description",
    "package_sizeof_sellingprice",
    "per_unit_sizedescription",
    "price_valid_from",
    "price_per_unit",
    "multi_buy_item_count",
    "multi_buy_items_price_total",
    "currency",
    "breadcrumb",
    "pdp_url",
    "variants",
    "product_description",
    "instructions",
    "storage_instructions",
    "preparationinstructions",
    "instructionforuse",
    "country_of_origin",
    "allergens",
    "age_of_the_product",
    "age_recommendations",
    "flavour",
    "nutritions",
    "nutritional_information",
    "vitamins",
    "labelling",
    "grade",
    "region",
    "packaging",
    "receipies",
    "processed_food",
    "barcode",
    "frozen",
    "chilled",
    "organictype",
    "cooking_part",
    "Handmade",
    "max_heating_temperature",
    "special_information",
    "label_information",
    "dimensions",
    "special_nutrition_purpose",
    "feeding_recommendation",
    "warranty",
    "color",
    "model_number",
    "material",
    "usp",
    "dosage_recommendation",
    "tasting_note",
    "food_preservation",
    "size",
    "rating",
    "review",
    "file_name_1",
    "image_url_1",
    "file_name_2",
    "image_url_2",
    "file_name_3",
    "image_url_3",
    "file_name_4",
    "image_url_4",
    "file_name_5",
    "image_url_5",
    "file_name_6",
    "image_url_6",
    "competitor_product_key",
    "fit_guide",
    "occasion",
    "material_composition",
    "style",
    "care_instructions",
    "heel_type",
    "heel_height",
    "upc",
    "features",
    "dietary_lifestyle",
    "manufacturer_address",
    "importer_address",
    "distributor_address",
    "vinification_details",
    "recycling_information",
    "return_address",
    "alchol_by_volume",
    "beer_deg",
    "netcontent",
    "netweight",
    "site_shown_uom",
    "ingredients",
    "random_weight_flag",
    "instock",
    "promo_limit",
    "product_unique_key",
    "multibuy_items_pricesingle",
    "perfect_match",
    "servings_per_pack",
    "Warning",
    "suitable_for",
    "standard_drinks",
    "environmental",
    "grape_variety",
    "retail_limit",
]