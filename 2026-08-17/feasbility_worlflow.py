

##############################CATEGORY_CRAWLER########################

import requests

headers = {
    }

json_data = {
    'query': '\n    \n    \n    \n    fragment ProductFields on Product {\n        attributes(keys: $attributes) {\n            key\n            value\n        }\n        activeCampaigns {\n            benefitQuantity\n            cartItemUsageLimit\n            description\n            discountType\n            discountValue\n            endTime\n            id\n            isAutoAddable\n            isBenefit\n            isTrigger\n            name\n            teaserFormat\n            totalTriggerThresholdFloat\n            triggerQuantity\n            type\n        }\n        badges\n        description\n        favourite\n        globalCatalogID\n        isAvailable\n        name\n        nmrAdID\n        originalPrice\n        packagingCharge\n        parentID\n        price\n        productBadges {\n            text\n            type\n            variant\n        }\n        productID\n        stockAmount\n        stockPrediction\n        tags\n        type\n        urls\n        vendorID\n        weightableAttributes {\n            weightedOriginalPrice\n            weightedPrice\n            weightValue {\n                unit\n                value\n            }\n        }\n    }\n\n    fragment ShopItemFields on ShopItem {\n        __typename\n        ...BannerFields\n        ...CategoryFields\n        ...ProductFields\n    }\n\n    fragment BannerFields on Banner {\n        bannerUrl\n        description\n        globalID\n        name\n        nmrAdID\n    }\n\n    fragment CategoryFields on Category {\n        categoryType\n        name\n        id\n        imageUrls\n        productTags\n    }\n\n    fragment ShopItemsListFields on ShopItemsList {\n        headline\n        localizedHeadline\n        requestID\n        shopItemID\n        shopItems {\n            ...ShopItemFields\n        }\n        shopItemType\n        swimlaneFilterType\n        trackingID\n        swimlaneTrackingKey\n    }\n\n    \n    fragment PageInfoFields on PageInfo {\n        isLast\n        pageNumber\n    }\n\n\n    fragment TrackingFields on Tracking {\n        experimentID\n        experimentVariation\n    }\n\n    fragment ShopItemsResponseFields on ShopItemsResponse {\n        shopItemsList {\n            ...ShopItemsListFields\n        }\n        pageInfo {\n            ...PageInfoFields\n        }\n        tracking {\n            ...TrackingFields\n        }\n    }\n\n\n    query getShopDetails(\n        $attributes: [String!]\n        $featureFlags: [FunWithFlag!]\n        $globalEntityId: String!\n        $isDarkstore: Boolean!\n        $locale: String!\n        $page: Int! = 0\n        $pastOrderStrategy: PastOrderStrategy\n        $userCode: String\n        $vendorCode: String!\n        $includeCategoryTree: Boolean!\n        $pageName: String!\n        $productIDs: [String!]\n        $productSKUs: [String!]\n        $complianceLevel: Int!\n    ) {\n        shopDetails {\n            categories(\n                input: {\n                    customerID: $userCode\n                    funWithFlags: $featureFlags\n                    globalEntityID: $globalEntityId\n                    isDarkstore: $isDarkstore\n                    locale: $locale\n                    pastOrderStrategy: $pastOrderStrategy\n                    platform: "web"\n                    vendorID: $vendorCode\n                }\n            ) @include(if: $includeCategoryTree) {\n                ...CategoryTreeFields\n            }\n            shopItemsResponse(\n                complianceLevel: $complianceLevel\n                input: {\n                    customerID: $userCode\n                    funWithFlags: $featureFlags\n                    globalEntityID: $globalEntityId\n                    isDarkstore: $isDarkstore\n                    locale: $locale\n                    pastOrderStrategy: $pastOrderStrategy\n                    platform: "web"\n                    vendorID: $vendorCode\n                }\n                page: $page\n                pageName: $pageName\n                swimlanesProps: {\n                    excludeProducts: true\n                    productIDs: $productIDs\n                    productSKUs: $productSKUs\n                }\n            ) {\n                ...ShopItemsResponseFields\n            }\n        }\n    }\n\n    fragment SubCategoryFields on SubCategory {\n        id\n        name\n        productsCount\n        productTags\n    }\n\n    fragment CategoryTreeFields on CategoryTree {\n        category {\n            ...CategoryFields\n        }\n        productsCount\n        subCategories {\n            ...SubCategoryFields\n        }\n        filters {\n            ... on CategoryFilter {\n                options {\n                    id\n                    name\n                }\n            }\n        }\n    }\n',
    'variables': {
        'attributes': [
            'baseContentValue',
            'baseUnit',
            'freshnessGuaranteeInDays',
            'maximumSalesQuantity',
            'minPriceLastMonth',
            'pricePerBaseUnit',
            'sku',
            'nutri_grade',
            'sugar_level',
        ],
        'complianceLevel': 5,
        'featureFlags': [
            {
                'key': 'pd-qc-weight-stepper',
                'value': 'Variation1',
            },
            {
                'key': 'qc-deal_zone-experiment',
                'value': 'Variation1',
            },
            {
                'key': 'qc-sort-offer-pills',
                'value': 'Variation1',
            },
        ],
        'globalEntityId': 'MJM_AT',
        'includeCategoryTree': False,
        'isDarkstore': False,
        'locale': 'de_AT',
        'page': 0,
        'pageName': 'shop_detail',
        'vendorCode': 'jrii',
    },
}

response = requests.post('https://mj.fd-api.com/api/v5/graphql', headers=headers, json=json_data)

#
data = response.json().get('data','').get('shopDetails','').get('shopItemsResponse','').get('shopItemsList','')

for section in data:
    headline = section["headline"]

    for item in section["shopItems"]:
        if item["__typename"] == "Category":
            category = item["name"]
            categorys =  item['id']

##############################CRAWLER##############################
import requests

headers = {
    }

json_data = {
    'query': '\n    \n    fragment ProductFields on Product {\n        attributes(keys: $attributes) {\n            key\n            value\n        }\n        activeCampaigns {\n            benefitQuantity\n            cartItemUsageLimit\n            description\n            discountType\n            discountValue\n            endTime\n            id\n            isAutoAddable\n            isBenefit\n            isTrigger\n            name\n            teaserFormat\n            totalTriggerThresholdFloat\n            triggerQuantity\n            type\n        }\n        badges\n        description\n        favourite\n        globalCatalogID\n        isAvailable\n        name\n        nmrAdID\n        originalPrice\n        packagingCharge\n        parentID\n        price\n        productBadges {\n            text\n            type\n            variant\n        }\n        productID\n        stockAmount\n        stockPrediction\n        tags\n        type\n        urls\n        vendorID\n        weightableAttributes {\n            weightedOriginalPrice\n            weightedPrice\n            weightValue {\n                unit\n                value\n            }\n        }\n    }\n\n\n    query getProductsByCategoryList(\n        $attributes: [String!]\n        $categoryId: String!\n        $featureFlags: [FunWithFlag!]\n        $filterOnSale: Boolean\n        $globalEntityId: String!\n        $isDarkstore: Boolean!\n        $locale: String!\n        $sort: ProductsSortType\n        $userCode: String\n        $vendorID: String!\n    ) {\n        categoryProductList(\n            input: {\n                categoryID: $categoryId\n                customerID: $userCode\n                filterOnSale: $filterOnSale\n                funWithFlags: $featureFlags\n                globalEntityID: $globalEntityId\n                isDarkstore: $isDarkstore\n                locale: $locale\n                platform: "web"\n                sort: $sort\n                vendorID: $vendorID\n            }\n        ) {\n            categoryProducts {\n                id\n                name\n                items {\n                    ...ProductFields\n                }\n            }\n        }\n    }\n',
    'variables': {
        'categoryId': 'ccf1c672-92a4-45a6-aeec-b5c78a306d6e',
        'attributes': [
            'baseContentValue',
            'baseUnit',
            'freshnessGuaranteeInDays',
            'maximumSalesQuantity',
            'minPriceLastMonth',
            'pricePerBaseUnit',
            'sku',
            'nutri_grade',
            'sugar_level',
        ],
        'featureFlags': [
            {
                'key': 'pd-qc-weight-stepper',
                'value': 'Variation1',
            },
        ],
        'filterOnSale': False,
        'globalEntityId': 'MJM_AT',
        'isDarkstore': False,
        'locale': 'de_AT',
        'sort': 'Recommended',
        'vendorID': 'jrii',
    },
}

response = requests.post('https://mj.fd-api.com/api/v5/graphql', headers=headers, json=json_data)

categoryProducts = response.json().get('data','').get('categoryProductList','').get('categoryProducts','')
for category in categoryProducts:
    for product in category.get("items", []):
        product_id = product.get("productID")
        product_name = product.get("name")

        selling_price =product.get("price")         # Current price
        regular_price = product.get("originalPrice") 


##############################PARSER##############################
import requests


 
headers = {
    }

json_data = {
    'query': '\n    \n    \n    \n    fragment ProductFields on Product {\n        attributes(keys: $attributes) {\n            key\n            value\n        }\n        activeCampaigns {\n            benefitQuantity\n            cartItemUsageLimit\n            description\n            discountType\n            discountValue\n            endTime\n            id\n            isAutoAddable\n            isBenefit\n            isTrigger\n            name\n            teaserFormat\n            totalTriggerThresholdFloat\n            triggerQuantity\n            type\n        }\n        badges\n        description\n        favourite\n        globalCatalogID\n        isAvailable\n        name\n        nmrAdID\n        originalPrice\n        packagingCharge\n        parentID\n        price\n        productBadges {\n            text\n            type\n            variant\n        }\n        productID\n        stockAmount\n        stockPrediction\n        tags\n        type\n        urls\n        vendorID\n        weightableAttributes {\n            weightedOriginalPrice\n            weightedPrice\n            weightValue {\n                unit\n                value\n            }\n        }\n    }\n\n    fragment ShopItemFields on ShopItem {\n        __typename\n        ...BannerFields\n        ...CategoryFields\n        ...ProductFields\n    }\n\n    fragment BannerFields on Banner {\n        bannerUrl\n        description\n        globalID\n        name\n        nmrAdID\n    }\n\n    fragment CategoryFields on Category {\n        categoryType\n        name\n        id\n        imageUrls\n        productTags\n    }\n\n    fragment ShopItemsListFields on ShopItemsList {\n        headline\n        localizedHeadline\n        requestID\n        shopItemID\n        shopItems {\n            ...ShopItemFields\n        }\n        shopItemType\n        swimlaneFilterType\n        trackingID\n        swimlaneTrackingKey\n    }\n\n    \n    fragment PageInfoFields on PageInfo {\n        isLast\n        pageNumber\n    }\n\n\n    fragment TrackingFields on Tracking {\n        experimentID\n        experimentVariation\n    }\n\n    fragment ShopItemsResponseFields on ShopItemsResponse {\n        shopItemsList {\n            ...ShopItemsListFields\n        }\n        pageInfo {\n            ...PageInfoFields\n        }\n        tracking {\n            ...TrackingFields\n        }\n    }\n\n    \n    \n    fragment FoodLabellingInfoFields on FoodLabellingInfo {\n        labelTitle\n        labelValues\n    }\n\n    fragment FoodLabellingFields on FoodLabelling {\n        additives {\n            ...FoodLabellingInfoFields\n        }\n        allergens {\n            ...FoodLabellingInfoFields\n        }\n        nutritionFacts {\n            ...FoodLabellingInfoFields\n        }\n        productClaims {\n            ...FoodLabellingInfoFields\n        }\n        productInfos {\n            ...FoodLabellingInfoFields\n        }\n        warnings {\n            ...FoodLabellingInfoFields\n        }\n    }\n\n    query getProductDetails(\n        $attributes: [String!]\n        $featureFlags: [FunWithFlag!]\n        $globalEntityId: String!\n        $locale: String!\n        $userCode: String\n        $vendorCode: String!\n        $productIdentifier: ProductIdentifier!\n        $crossSellProductsComplianceLevel: Int!\n        $crossSellProductsIsDarkstore: Boolean!\n        $includeCrossSell: Boolean!\n    ) {\n        productDetails(\n            input: {\n                customerID: $userCode\n                funWithFlags: $featureFlags\n                globalEntityID: $globalEntityId\n                locale: $locale\n                productIdentifier: $productIdentifier\n                vendorID: $vendorCode\n            }\n        ) {\n            crossSellProducts(\n                platform: "web"\n                complianceLevel: $crossSellProductsComplianceLevel\n                isDarkstore: $crossSellProductsIsDarkstore\n            ) @include(if: $includeCrossSell) {\n                ...ShopItemsResponseFields\n            }\n            product {\n                ...ProductDetailsFields\n            }\n        }\n    }\n\n    fragment ProductDetailsFields on Product {\n        ...ProductFields\n        foodLabelling {\n            ...FoodLabellingFields\n        }\n    }\n',
    'variables': {
        'featureFlags': [
            {
                'key': 'pd-qc-weight-stepper',
                'value': 'Variation1',
            },
        ],
        'globalEntityId': 'MJM_AT',
        'locale': 'de_AT',
        'vendorCode': 'jrii',
        'productIdentifier': {
            'type': 'ID',
            'value': '25145495',
        },
        'crossSellProductsComplianceLevel': 7,
        'crossSellProductsIsDarkstore': False,
        'includeCrossSell': True,
    },
}
json_data["variables"]["productIdentifier"]["value"] = product_id
response = requests.post('https://mj.fd-api.com/api/v5/graphql', headers=headers, json=json_data)

data = response.json().get('data','').get('productDetails','').get('product','')
data


nutrition_facts = data.get("foodLabelling", {}).get("nutritionFacts", [])

nutritional_information = "; ".join(
    f"{x['labelTitle']}: {x['labelValues'][0]}"
    for x in nutrition_facts
)

product_id = data.get('productID','')

product_name = data.get('name')

product_unique_key = str(product_id)+"P"
selling_price = data.get('price','')

regular_price = data.get('originalPrice','')

product_infos = data.get('foodLabelling',{}).get('productInfos',[])

image_1 =data.get('urls')

netweight = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Nettofüllmenge"
)

product_name = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Produktname"
)

product_description = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Produktbeschreibung"
)

country_of_origin  = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Ursprungsland"
)

currency = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Pfand (Währung)"
)


attributes = data.get("attributes",'')

attrs = {item["key"]: item["value"] for item in attributes}

gram_unit = attrs.get("contentsUnit")
gram_quantity = float(attrs.get("contentsValue", 0))
gram_quantity, gram_unit

site_shown_uom = f"{gram_quantity:g} {gram_unit}" if gram_quantity and gram_unit else ""

ingredients = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Zutaten (Allergene hervorgehoben in Großbuchstaben)"
    or x["labelTitle"] == "Zutaten"
)

storage_instructions  = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Aufbewahrungshinweis"

)

instructionforuse = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Verwendungshinweis"
)

size = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Größe"
)


special_information = next(
    x["labelValues"][0]
    for x in product_infos
    if x["labelTitle"] == "Weitere Informationen"
)

retail_limit = attrs.get('maximumSalesQuantity','')

barcode = attrs.get("pieceBarcodes",'')
price__base  = attrs.get('pricePerBaseUnit','')

unit_base =  attrs.get('baseUnit','')

vaule_base = attrs.get('baseContentValue','')

price_per_base_unit = (
    f"{float(price__base):.2f} € je "
    f"{vaule_base} {unit_base}"
)
product_decsription = data.get('description','')
price_per_base_unit