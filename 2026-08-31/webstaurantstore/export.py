import csv
import logging
from settings import (
    MONGO_COLLECTION_PRODUCT_DATA,
    file_name,
    FILE_HEADERS,
    client,
    MONGO_DB
)


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

            product_url = item.get("product_url", "")
            name = item.get("name", "")
            brand = item.get("brand", "")
            sku = item.get("sku", "")
            rating = item.get("rating", "")
            shipping_info = item.get("shipping_info", "")
            upc = item.get("upc", "")
            document = item.get("documnet", "")
            category = item.get("category", "")
            item_number = item.get("item_number", "")
            video = item.get("video", "")
            price = item.get("price", "")
            price_unit = item.get("price_unit", "")
            product_details = item.get("product_details", "")
            features = item.get("features", "")
            selected_variant =  item.get("selected_variant", {})
            configurable_attributes = item.get("configurable_attributes","")
            specifications = item.get("specifications", {})
            related_product_skus = item.get("related_product_skus","")
            faq = item.get( "faq", "")
            images = item.get("images","")
            configurable_variations = item.get("Configurable Variations", [])
            m_3Dmodel = item.get( "m_3Dmodel", "")
            breadcrumbs = item.get("breadcrumbs","")


            data = [
                product_url,
                name,
                brand,
                sku,
                rating,
                shipping_info,
                upc,
                document,
                category,
                item_number,
                video,
                price,
                price_unit,
                product_details,
                features,
                selected_variant,
                configurable_attributes,
                specifications,
                related_product_skus,
                faq,
                images,
                configurable_variations,
                m_3Dmodel,
                breadcrumbs,
            ]

            self.writer.writerow(data)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    with open(file_name, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        export = Export(writer)
        export.start()

    