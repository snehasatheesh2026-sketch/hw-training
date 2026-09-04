from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField
from settings import (
   MONGO_COLLECTION_DATA,
     MONGO_COLLECTION_PRODUCT_DATA
     , MONGO_COLLECTION_CATEGORY,
)





class ProductCategoryUrlItem(DynamicDocument):

    meta = {
        "db_alias": "default",
        "collection": MONGO_COLLECTION_CATEGORY
    }

    end_category_name = StringField(
        required=True
    )

    end_category_url = StringField(
        required=True,
        unique=True
    )