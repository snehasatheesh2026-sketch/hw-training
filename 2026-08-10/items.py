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
    
    