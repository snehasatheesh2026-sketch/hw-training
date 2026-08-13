from datetime import datetime
import os
import calendar
import logging
import configparser
import pytz
from dateutil.relativedelta import relativedelta, MO
import requests
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


PROJECT = "matalanme"
CLIENT_NAME = ""
PROJECT_NAME = "matalanme"
FREQUENCY = "ONETIME"
BASE_URL = "https://www.matalanme.com/ae_en"

JOIN_URL = "https://www.matalanme.com/ae_en/"


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
MONGO_DB = f"matalanme{iteration}"
MONGO_COLLECTION_RESPONSE = f"{PROJECT_NAME}_url"
MONGO_COLLECTION_CATEGORY = f"{PROJECT_NAME}_category_url"
MONGO_COLLECTION_URL_FAILED = f"{PROJECT_NAME}_url_failed"
MONGO_COLLECTION_DATA = f"{PROJECT_NAME}_data"
MONGO_COLLECTION_PRODUCT_DATA =f"{PROJECT_NAME}_product_data"

connect(
    db=MONGO_DB,
    host="mongodb://localhost:27017",
    alias="default")

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.matalanme.com',
    'referer': 'https://www.matalanme.com/',
    'store': 'matalan_ae_en',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'website': 'matalan',


    }
file_name ="roductss.csv"



FILE_HEADERS = [
    "url",
    "product_id",
    "product_name",
    "extraction_date",
    "regular_price",
    "sellings_price",
    "currency",
    "description",
    "breadcrumb",
    "quantity",
    "product_details",
    "colors",
    "sizes",
    "gender",
    "images",
]

params = {
    "product_version": "2035",
    "query": """query GetProductList(
        $filter: ProductAttributeFilterInput,
        $pageSize: Int,
        $currentPage: Int,
        $sort: ProductAttributeSortInput
    ) {
        products(
            filter: $filter
            pageSize: $pageSize
            currentPage: $currentPage
            sort: $sort
        ) {
            total_count

            page_info {
                current_page
                page_size
                total_pages
            }

            items {
                id
                sku
                name
                url_key
                brand_name
                home_delivery
                store_pickup
                product_label
                stock_status
                is_new
                is_bestseller
                is_featured
                hover_image
                rating_aggregation_value

                thumbnail {
                    url
                    label
                }

                categories {
                    id
                    name
                }

                price_range {
                    minimum_price {
                        regular_price {
                            value
                            currency
                        }
                        final_price {
                            value
                            currency
                        }
                        discount {
                            amount_off
                            percent_off
                        }
                    }
                }
            }
        }
    }""",

    "operationName": "GetProductList",

    "variables": json.dumps({
        "filter": {
            "category_uid": {
                "in": ["MTky"]
            }
        },
        "pageSize": 40,
        "currentPage": 1,
        "sort": {}
    })
}

API_URL = "https://api.bfab.com/graphql"