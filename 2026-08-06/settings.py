from datetime import datetime
import os
import calendar
import logging
import configparser
import pytz
from dateutil.relativedelta import relativedelta, MO
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


PROJECT = "webstaurantstore"
CLIENT_NAME = ""
PROJECT_NAME = "webstaurantstore"
FREQUENCY = "ONETIME"
BASE_URL = "https://www.webstaurantstore.com"


datetime_obj = datetime.now(pytz.timezone("Asia/Kolkata"))

iteration = datetime_obj.strftime("%Y_%m_%d")
YEAR = datetime_obj.strftime("%Y")
MONTH = datetime_obj.strftime("%m")
DAY = datetime_obj.strftime("%d")
MONTH_VALUE = calendar.month_abbr[int(MONTH.lstrip("0"))]
WEEK = (int(DAY) - 1) // 7 + 1

FILE_NAME = f"webstaurantstore{iteration}"

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

from mongoengine import connect



# Mongo db and collections	
MONGO_DB = f"webstaurantstore{iteration}"
MONGO_COLLECTION_RESPONSE = f"{PROJECT_NAME}_url"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_DATA = f"{PROJECT_NAME}_data"

MONGO_COLLECTION_PRODUCT_DATA =f"{PROJECT_NAME}_PRODUCT_data"
HEADERS = {
}


COOKIES = {
              
}
connect(
    db=MONGO_DB,
    host="mongodb://localhost:27017/",
    alias="default")
file_name ="webstaurantstore_products.csv"



FILE_HEADERS = [
    "product_url",
    "name",
    "brand",
    "SKU",
    "rating",
    "shipping_info",
    "upc",
    "documnet",
    "category",
    "item_number",
    "video",
    "price",
    "price_unit",
    "product_details",
    "features",
    "selected_variant",
    "configurable_attributes",
    "specifications",
    "related_product_skus",
    "FAQ",
    "images",
    "Configurable Variations",
    "m_3Dmodel",
    "breadcrumbs",
]


