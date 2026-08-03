from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField
from settings import (
   MONGO_COLLECTION_URL_FAILED,
   MONGO_COLLECTION_DATA,
     MONGO_COLLECTION_PRODUCT_DATA,
   MONGO_COLLECTION_RESPONSE, MONGO_COLLECTION_CATEGORY,
)

class ProductCategoryUrlItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    
    category_name = StringField(required=True)


    url = StringField(required=True)

class ProductItem(DynamicDocument):
    """initializing URL fields and its Data-Types"""

    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_DATA}
    url = StringField()
    category_name = StringField(required=True)
    product_name = StringField()

from mongoengine import DynamicDocument, StringField, DictField

from mongoengine import DynamicDocument, StringField, DictField

class ProductdataItem(DynamicDocument):
    """Product details schema"""

    meta = {
        "db_alias": "default",
        "collection": MONGO_COLLECTION_PRODUCT_DATA,
    }

    product_url = StringField()
    name = StringField()
    rating = StringField()
    shipping_info = StringField()
    upc = StringField()
    document = StringField()
    category = StringField(required=True)
    item_number = StringField()
    video = StringField()
    price = StringField()
    price_unit = StringField()
    product_details = StringField()
    features = StringField()
    selected_variant = DictField()
    configurable_attributes = StringField()
    specifications = DictField()
    related_product_skus = StringField()