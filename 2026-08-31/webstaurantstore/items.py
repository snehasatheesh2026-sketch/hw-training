from mongoengine import DynamicDocument, StringField, BooleanField, DictField, ListField, IntField, FloatField
from settings import (
   MONGO_COLLECTION_DATA,
     MONGO_COLLECTION_PRODUCT_DATA
     , MONGO_COLLECTION_CATEGORY,
)

class ProductCategoryUrlItem(DynamicDocument):


    meta = {"db_alias": "default", "collection": MONGO_COLLECTION_CATEGORY}
    
    category_name = StringField(required=True)


    url = StringField(
        required=True,
        unique=True
    )


class ProductItem(DynamicDocument):

    meta = {
        "db_alias": "default",
        "collection": MONGO_COLLECTION_DATA
    }

    product_url = StringField(
        required=True,
        unique=True
    )

    category_name = StringField(
        required=True
    )

    product_name = StringField()

    item_number = StringField()


class ProductdataItem(DynamicDocument):


    meta = {
        "db_alias": "default",
        "collection": MONGO_COLLECTION_PRODUCT_DATA,
    }

    product_url = StringField( 
         required=True,
         unique=True
    )
    name = StringField()
    brand = StringField()
    sku = StringField()
    rating = StringField()
    shipping_info = StringField()
    upc = StringField()
    document = StringField()
    category = StringField()
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
    faq = StringField()
    images = StringField()
    configurable_variations = ListField()
    m_3Dmodel = StringField()
    breadcrumbs = StringField()