import requests

import re

import json

##############################CRAWLER##############################

cookies = {
      'MCLVALID': ''
}

headers = {
    }

params = {
    'page': '1',
    'view': 'json',
}

response = requests.get('https://bevmo.com/collections/whiskies', params=params, cookies=cookies, headers=headers)



data =response.json()


total_pages = data.get('paginate', {}).get('pages')


product_ids = data.get('productIds', '')

product_ids = [int(x) for x in data.get('productIds', '').split(',')]

for page in range(1, total_pages + 1):

    print(f"Scraping page {page}/{total_pages}")

    params = {
        'page': page,
        'view': 'json',
    }

    response = requests.get(
        'https://bevmo.com/collections/whiskies',
        params=params,
        cookies=cookies,
        headers=headers
    )

    data = response.json()

    # Get product IDs and convert them to integers
    product_ids = [
        int(x.strip())
        for x in data.get('productIds', '').split(',')
        if x.strip()
    ]

    json_data = {
    'fulfillment_type': 'pickup',
    'selected_taxonomy': '',
    'location_id': 1,
    'filters': {},
    'sort_by': '',
    'per_page': 24,
    'adSessionId': '63a2d092-c24a-4261-afa8-12382530ede8',
    'pageType': 'COLLECTION',
    'contentRequestId': '3p-crq-4e17c073-1b6c-4070-bf17-48cbb02e9dd1',
    'ids': [
        15719,
        3144,
        208523,
        67383,
        7569,
        8658,
        8656,
        12094,
        21550,
        12128,
        17257,
        12127,
        33976,
        12126,
        56043,
        11998,
        17377,
        12137,
        12135,
        71557,
        18568,
        15932,
        12138,
        33977,
    ],
    'sortOptions': [
        {
            'label': 'Featured',
            'key': 'manual',
        },
        {
            'label': 'Most relevant',
            'key': 'most-relevant',
        },
        {
            'label': 'Best selling',
            'key': 'best-selling',
        },
        {
            'label': 'Alphabetically, A-Z',
            'key': 'title-ascending',
        },
        {
            'label': 'Alphabetically, Z-A',
            'key': 'title-descending',
        },
        {
            'label': 'Price, low to high',
            'key': 'price-ascending',
        },
        {
            'label': 'Price, high to low',
            'key': 'price-descending',
        },
        {
            'label': 'Date, old to new',
            'key': 'created-ascending',
        },
        {
            'label': 'Date, new to old',
            'key': 'created-descending',
        },
    ],
    'filterOptions': [
        {
            'type': 'list',
            'label': 'Deals',
            'key': 'p.tag',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': '15offprem',
                    'key': '15offprem',
                    'param_name': 'filter.p.tag',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '15offprem-az',
                    'key': '15offprem-az',
                    'param_name': 'filter.p.tag',
                    'count': 8,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '15offprem-ca',
                    'key': '15offprem-ca',
                    'param_name': 'filter.p.tag',
                    'count': 37,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '15offprem-wa',
                    'key': '15offprem-wa',
                    'param_name': 'filter.p.tag',
                    'count': 14,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': "30% off for 30 years of cheer at BevMo's",
                    'key': 'gid://shopify/FilterSettingGroup/110330153',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'bogo-az',
                    'key': 'bogo-az',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'bogo-ca',
                    'key': 'bogo-ca',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'bogo-wa',
                    'key': 'bogo-wa',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection-az',
                    'key': 'collection-az',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection-ca',
                    'key': 'collection-ca',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection-wa',
                    'key': 'collection-wa',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection_spirit-az',
                    'key': 'collection_spirit-az',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection_spirit-ca',
                    'key': 'collection_spirit-ca',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'collection_spirit-wa',
                    'key': 'collection_spirit-wa',
                    'param_name': 'filter.p.tag',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'lastchance',
                    'key': 'lastchance',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'lastchance-az',
                    'key': 'lastchance-az',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'lastchance-ca',
                    'key': 'lastchance-ca',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'lastchance-wa',
                    'key': 'lastchance-wa',
                    'param_name': 'filter.p.tag',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'superbowl_alcohol',
                    'key': 'superbowl_alcohol',
                    'param_name': 'filter.p.tag',
                    'count': 37,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'superbowl_alcohol-az',
                    'key': 'superbowl_alcohol-az',
                    'param_name': 'filter.p.tag',
                    'count': 134,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'superbowl_alcohol-ca',
                    'key': 'superbowl_alcohol-ca',
                    'param_name': 'filter.p.tag',
                    'count': 134,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'superbowl_alcohol-wa',
                    'key': 'superbowl_alcohol-wa',
                    'param_name': 'filter.p.tag',
                    'count': 134,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'tiered_case_sale-az',
                    'key': 'tiered_case_sale-az',
                    'param_name': 'filter.p.tag',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'tiered_case_sale-ca',
                    'key': 'tiered_case_sale-ca',
                    'param_name': 'filter.p.tag',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'tiered_case_sale-wa',
                    'key': 'tiered_case_sale-wa',
                    'param_name': 'filter.p.tag',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Category',
            'key': 'p.m.gopuff.subclass',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Whisky - Canadian',
                    'key': 'Whisky - Canadian',
                    'param_name': 'filter.p.m.gopuff.subclass',
                    'count': 125,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Whisky - Japanese',
                    'key': 'Whisky - Japanese',
                    'param_name': 'filter.p.m.gopuff.subclass',
                    'count': 81,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Whisky - Rest of World',
                    'key': 'Whisky - Rest of World',
                    'param_name': 'filter.p.m.gopuff.subclass',
                    'count': 18,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Varietal & Type',
            'key': 'p.m.gopuff.product_type',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Blended',
                    'key': 'Blended',
                    'param_name': 'filter.p.m.gopuff.product_type',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Flavored',
                    'key': 'Flavored',
                    'param_name': 'filter.p.m.gopuff.product_type',
                    'count': 43,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Other Whiskey - American',
                    'key': 'Other Whiskey - American',
                    'param_name': 'filter.p.m.gopuff.product_type',
                    'count': 10,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Size',
            'key': 'p.m.gopuff.size',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': '1L',
                    'key': '1L',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1.75L',
                    'key': '1.75L',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 21,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '50ml',
                    'key': '50ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 25,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '100ml',
                    'key': '100ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '200ml',
                    'key': '200ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '375ml',
                    'key': '375ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 5,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '700ml',
                    'key': '700ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 21,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '750ml',
                    'key': '750ml',
                    'param_name': 'filter.p.m.gopuff.size',
                    'count': 146,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Country',
            'key': 'p.m.gopuff.origination_country',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Canada',
                    'key': 'Canada',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 111,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'France',
                    'key': 'France',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'India',
                    'key': 'India',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Japan',
                    'key': 'Japan',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Mexico',
                    'key': 'Mexico',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Taiwan',
                    'key': 'Taiwan',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'United States',
                    'key': 'United States',
                    'param_name': 'filter.p.m.gopuff.origination_country',
                    'count': 17,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Region',
            'key': 'p.m.gopuff.origination_region',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Oregon',
                    'key': 'Oregon',
                    'param_name': 'filter.p.m.gopuff.origination_region',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Brand',
            'key': 'p.vendor',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': '8 Seconds',
                    'key': '8 Seconds',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Abasolo',
                    'key': 'Abasolo',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Akashi',
                    'key': 'Akashi',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Alberta',
                    'key': 'Alberta',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Amrut',
                    'key': 'Amrut',
                    'param_name': 'filter.p.vendor',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Bearface',
                    'key': 'Bearface',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'BevMo!',
                    'key': 'BevMo!',
                    'param_name': 'filter.p.vendor',
                    'count': 33,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Black Velvet',
                    'key': 'Black Velvet',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Brenne',
                    'key': 'Brenne',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Bushmills',
                    'key': 'Bushmills',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Canadian Club',
                    'key': 'Canadian Club',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Canadian Mist',
                    'key': 'Canadian Mist',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Canadian Ridge',
                    'key': 'Canadian Ridge',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Chichibu',
                    'key': 'Chichibu',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Crown Royal',
                    'key': 'Crown Royal',
                    'param_name': 'filter.p.vendor',
                    'count': 42,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Fireball',
                    'key': 'Fireball',
                    'param_name': 'filter.p.vendor',
                    'count': 18,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Forty Creek',
                    'key': 'Forty Creek',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Fukano',
                    'key': 'Fukano',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'FUYU',
                    'key': 'FUYU',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Glenfiddich',
                    'key': 'Glenfiddich',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Gyokusendo Peak',
                    'key': 'Gyokusendo Peak',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Hakushu',
                    'key': 'Hakushu',
                    'param_name': 'filter.p.vendor',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Hatozaki',
                    'key': 'Hatozaki',
                    'param_name': 'filter.p.vendor',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Hibiki',
                    'key': 'Hibiki',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Hinotori',
                    'key': 'Hinotori',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Iwai',
                    'key': 'Iwai',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': "JP Wiser's",
                    'key': 'JP Wiser&#39;s',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kaiyo',
                    'key': 'Kaiyo',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kamiki',
                    'key': 'Kamiki',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kavalan',
                    'key': 'Kavalan',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kikori',
                    'key': 'Kikori',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kisoyama',
                    'key': 'Kisoyama',
                    'param_name': 'filter.p.vendor',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kojiki',
                    'key': 'Kojiki',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kujira',
                    'key': 'Kujira',
                    'param_name': 'filter.p.vendor',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Kurayoshi',
                    'key': 'Kurayoshi',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Lot 40',
                    'key': 'Lot 40',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'MacNaughton',
                    'key': 'MacNaughton',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Matsui',
                    'key': 'Matsui',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Minden Mill',
                    'key': 'Minden Mill',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Nikka',
                    'key': 'Nikka',
                    'param_name': 'filter.p.vendor',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Nobushi',
                    'key': 'Nobushi',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Ohishi',
                    'key': 'Ohishi',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Pendleton',
                    'key': 'Pendleton',
                    'param_name': 'filter.p.vendor',
                    'count': 8,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Rampur',
                    'key': 'Rampur',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Revel Stoke',
                    'key': 'Revel Stoke',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Rich & Rare',
                    'key': 'Rich &amp; Rare',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Royal Challenge',
                    'key': 'Royal Challenge',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Sasakawa',
                    'key': 'Sasakawa',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': "Seagram's Spirits",
                    'key': 'Seagram&#39;s Spirits',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Shibui',
                    'key': 'Shibui',
                    'param_name': 'filter.p.vendor',
                    'count': 7,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Shinobu',
                    'key': 'Shinobu',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Sierra Norte',
                    'key': 'Sierra Norte',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Sinfire',
                    'key': 'Sinfire',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Snake River',
                    'key': 'Snake River',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Suntory',
                    'key': 'Suntory',
                    'param_name': 'filter.p.vendor',
                    'count': 4,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Tenjaku',
                    'key': 'Tenjaku',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'The San-In',
                    'key': 'The San-In',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'The Solan',
                    'key': 'The Solan',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Three Fingers',
                    'key': 'Three Fingers',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Togouchi',
                    'key': 'Togouchi',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Tottori',
                    'key': 'Tottori',
                    'param_name': 'filter.p.vendor',
                    'count': 2,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Unknown',
                    'key': 'Unknown',
                    'param_name': 'filter.p.vendor',
                    'count': 5,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Windsor',
                    'key': 'Windsor',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Yamazaki',
                    'key': 'Yamazaki',
                    'param_name': 'filter.p.vendor',
                    'count': 6,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Yukon Jack',
                    'key': 'Yukon Jack',
                    'param_name': 'filter.p.vendor',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Store',
            'key': 'p.m.gopuff.available_locations',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': '398',
                    'key': '398',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '399',
                    'key': '399',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 79,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '400',
                    'key': '400',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '401',
                    'key': '401',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '402',
                    'key': '402',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '403',
                    'key': '403',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '404',
                    'key': '404',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '405',
                    'key': '405',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 76,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '406',
                    'key': '406',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 87,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '407',
                    'key': '407',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '408',
                    'key': '408',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '409',
                    'key': '409',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '410',
                    'key': '410',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 93,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '411',
                    'key': '411',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '412',
                    'key': '412',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 62,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '413',
                    'key': '413',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '414',
                    'key': '414',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '415',
                    'key': '415',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '416',
                    'key': '416',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '417',
                    'key': '417',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '418',
                    'key': '418',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 67,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '419',
                    'key': '419',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '420',
                    'key': '420',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '421',
                    'key': '421',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '422',
                    'key': '422',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '423',
                    'key': '423',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '424',
                    'key': '424',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 62,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '425',
                    'key': '425',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 66,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '426',
                    'key': '426',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '427',
                    'key': '427',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '428',
                    'key': '428',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 81,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '429',
                    'key': '429',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '434',
                    'key': '434',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '435',
                    'key': '435',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 84,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '436',
                    'key': '436',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 86,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '437',
                    'key': '437',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '438',
                    'key': '438',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '439',
                    'key': '439',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '440',
                    'key': '440',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 80,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '441',
                    'key': '441',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '442',
                    'key': '442',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '444',
                    'key': '444',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '445',
                    'key': '445',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '446',
                    'key': '446',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '447',
                    'key': '447',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 82,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '448',
                    'key': '448',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 64,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '449',
                    'key': '449',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '450',
                    'key': '450',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 88,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '451',
                    'key': '451',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 62,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '452',
                    'key': '452',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 80,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '453',
                    'key': '453',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '454',
                    'key': '454',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '455',
                    'key': '455',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '456',
                    'key': '456',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 76,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '457',
                    'key': '457',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '458',
                    'key': '458',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '459',
                    'key': '459',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '460',
                    'key': '460',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 67,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '461',
                    'key': '461',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '462',
                    'key': '462',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '463',
                    'key': '463',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '464',
                    'key': '464',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 86,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '465',
                    'key': '465',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '466',
                    'key': '466',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '467',
                    'key': '467',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '468',
                    'key': '468',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '469',
                    'key': '469',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '470',
                    'key': '470',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '471',
                    'key': '471',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '472',
                    'key': '472',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '473',
                    'key': '473',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '474',
                    'key': '474',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '475',
                    'key': '475',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 61,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '482',
                    'key': '482',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 80,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '483',
                    'key': '483',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 84,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '485',
                    'key': '485',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 79,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '487',
                    'key': '487',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 88,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '489',
                    'key': '489',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '490',
                    'key': '490',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 80,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '491',
                    'key': '491',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 83,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '492',
                    'key': '492',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '494',
                    'key': '494',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '495',
                    'key': '495',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '496',
                    'key': '496',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 79,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '497',
                    'key': '497',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '498',
                    'key': '498',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '499',
                    'key': '499',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '500',
                    'key': '500',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '501',
                    'key': '501',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '502',
                    'key': '502',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '503',
                    'key': '503',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '504',
                    'key': '504',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 81,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '505',
                    'key': '505',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 61,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '506',
                    'key': '506',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '507',
                    'key': '507',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '508',
                    'key': '508',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '509',
                    'key': '509',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '510',
                    'key': '510',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '511',
                    'key': '511',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 85,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '512',
                    'key': '512',
                    'param_name': 'filter.p.m.gopuff.available_locations',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Store',
            'key': 'p.m.gopuff.available_locations_2',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': '777',
                    'key': '777',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '778',
                    'key': '778',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 65,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '779',
                    'key': '779',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '780',
                    'key': '780',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '781',
                    'key': '781',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 85,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '782',
                    'key': '782',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '783',
                    'key': '783',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '784',
                    'key': '784',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '785',
                    'key': '785',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '786',
                    'key': '786',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 84,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1016',
                    'key': '1016',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1017',
                    'key': '1017',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1019',
                    'key': '1019',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 86,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1020',
                    'key': '1020',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1021',
                    'key': '1021',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1117',
                    'key': '1117',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1118',
                    'key': '1118',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1119',
                    'key': '1119',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1152',
                    'key': '1152',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1434',
                    'key': '1434',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1435',
                    'key': '1435',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1436',
                    'key': '1436',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 70,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1437',
                    'key': '1437',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 73,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1438',
                    'key': '1438',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1439',
                    'key': '1439',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1440',
                    'key': '1440',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 59,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1441',
                    'key': '1441',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 81,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1442',
                    'key': '1442',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 75,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1443',
                    'key': '1443',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 72,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1444',
                    'key': '1444',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 78,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1445',
                    'key': '1445',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1446',
                    'key': '1446',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1447',
                    'key': '1447',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1448',
                    'key': '1448',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1449',
                    'key': '1449',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 71,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1450',
                    'key': '1450',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 67,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1451',
                    'key': '1451',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 68,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1452',
                    'key': '1452',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 74,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1453',
                    'key': '1453',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 77,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1454',
                    'key': '1454',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 69,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1456',
                    'key': '1456',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 79,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': '1476',
                    'key': '1476',
                    'param_name': 'filter.p.m.gopuff.available_locations_2',
                    'count': 76,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Deals(AZ)',
            'key': 'p.m.gopuff.active_buy_get_offers_text_az',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Buy 2, Save More',
                    'key': 'gid://shopify/FilterSettingGroup/172523817',
                    'param_name': 'filter.p.m.gopuff.active_buy_get_offers_text_az',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'Buy 6 for $18',
                    'key': 'gid://shopify/FilterSettingGroup/169836841',
                    'param_name': 'filter.p.m.gopuff.active_buy_get_offers_text_az',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Deals(CA)',
            'key': 'p.m.gopuff.active_buy_get_offers_text_ca',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Buy 2, Save More',
                    'key': 'gid://shopify/FilterSettingGroup/172491049',
                    'param_name': 'filter.p.m.gopuff.active_buy_get_offers_text_ca',
                    'count': 1,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'list',
            'label': 'Deals(WA)',
            'key': 'p.m.gopuff.active_buy_get_offers_text_wa',
            'presentation': 'text',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Buy 6 for $18',
                    'key': 'gid://shopify/FilterSettingGroup/169935145',
                    'param_name': 'filter.p.m.gopuff.active_buy_get_offers_text_wa',
                    'count': 3,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'boolean',
            'label': 'Deals(AZ)',
            'key': 'p.m.gopuff.has_clubbev_pricing_az',
            'presentation': '',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Yes',
                    'key': '1',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_az',
                    'count': 20,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'No',
                    'key': '0',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_az',
                    'count': 159,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'boolean',
            'label': 'Deals(CA)',
            'key': 'p.m.gopuff.has_clubbev_pricing_ca',
            'presentation': '',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Yes',
                    'key': '1',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_ca',
                    'count': 46,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'No',
                    'key': '0',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_ca',
                    'count': 133,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
        {
            'type': 'boolean',
            'label': 'Deals(WA)',
            'key': 'p.m.gopuff.has_clubbev_pricing_wa',
            'presentation': '',
            'operator': 'OR',
            'url_to_remove': '/collections/whiskies?view=json',
            'options': [
                {
                    'label': 'Yes',
                    'key': '1',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_wa',
                    'count': 17,
                    'swatch': None,
                    'active': False,
                },
                {
                    'label': 'No',
                    'key': '0',
                    'param_name': 'filter.p.m.gopuff.has_clubbev_pricing_wa',
                    'count': 162,
                    'swatch': None,
                    'active': False,
                },
            ],
            'active_values': [],
        },
    ],
    'offset': 0,
    'shopify_shop_domain': 'bevmo-ca.myshopify.com',
    'unified': True,
}
    json_data['ids'] =  product_ids
    response = requests.post('https://bevmo.com/shopify/v1/bevmo/shops/products', cookies=cookies, headers=headers, json=json_data)
    data = response.json()

    datas = data.get('products','')

    for i in datas:
      product_name = i.get('title','')

      product_id = i.get('id','')

      images = i.get('image',{})

      tags = i.get('tags','')

      is_alcohol = i.get('is_alcohol','')

      is_tobacco = i.get('is_tobacco','')

      regular_price = i.get('price','')

      offer_price = i.get('offer','')


##############################PARSER##############################



cookies = {

        'MCLVALID': ''
       }

headers = {
    }



response = requests.get(f'https://bevmo.com/products/{product_id}', cookies=cookies, headers=headers)
from parsel import Selector

selector = Selector(text=response.text)

pdp_url =selector.xpath('//link[@rel="canonical"]/@href').get()


unique_id =  selector.xpath('//product-info/@data-gopuff-product-id').get()

# product_name = selector.xpath('//meta[@property="og:title"]/@content').get()
# regular_price = selector.xpath('//meta[@property="og:price:amount"]/@content').get()

# product_schema = selector.xpath(  '//script[@id="ProductSchema"]/text()').get()

# product_data = json.loads(product_schema)

# offer_price  = product_data.get('offers', [{}])[0].get('price')

# offer_price = float(offer_price)

if float(regular_price) == offer_price:
    offer_price = ""
    selling_price = regular_price
else:
    selling_price = offer_price

currency = selector.xpath('//meta[@property="og:price:currency"]/@content').get()


Image = selector.xpath( '//div[contains(@class, "product-media-container")]//img/@src').getall()

product_description = selector.xpath('//meta[@name="description"]/@content').get()


warning = selector.xpath( '//p[contains(@class, "warning")]//text()').getall()

warning= ' '.join(text.strip() for text in warning if text.strip())


details = selector.xpath('//div[contains(@class, "product-details")]//li')

product_details = {}

for detail in details:
    label = detail.xpath(
        './/span[contains(@class, "product-details--list-label")]/text()'
    ).get()

    value = detail.xpath(
        './/span[contains(@class, "product-details--list-value")]/text()'
    ).get()

    if label and value:
        product_details[label.strip()] = value.strip()


size = product_details.get('Size', '')

alcohol_content = product_details.get('ABV', '')

country_of_origin = product_details.get('Country', '')

sku = product_details.get('SKU', '')


product_text = ' '.join(selector.xpath( '//p[contains(@class, "product__text")]//text()').getall()).strip()


match = re.search(r'([\d.]+)\s*([a-zA-Z]+)', product_text)

if match:
   
   grammage_quantity  = match.group(1)

   grammage_unit = match.group(2)

site_shown_uom = f"{grammage_quantity}{grammage_unit}"


special_information = selector.xpath( '//h4[contains(., "Government Issued ID Required for Purchase")]/following-sibling::p[1]/text()').get()


script = selector.xpath( '//script[contains(., "ShopifyAnalytics.lib.track")]/text()').get()


breadcrumbs = re.search(r'"category":"([^"]+)"', script).group(1)


brand = re.search(r'"brand":"([^"]+)"', script).group(1)



script_text = '\n'.join(selector.xpath('//script/text()').getall())

matchs = re.search(
    r'inventory_in_stock_show_count:\s*`([^`]*)`',
    script_text
)

if matchs:
     inventory_text = matchs.group(1)
     if "in stock" in inventory_text.lower():

          stock_availblity = "in_stock"
     else:
          stock_availblity = "out_of_stock"




# --------------------------------------------------------------------------------------------------------------------------


from urllib.parse import urljoin
from parsel import Selector
import requests

cookies ={}
headers = {
}

response = requests.get('https://bevmo.com/', cookies=cookies, headers=headers)
selector = Selector(text=response.text)

# Categories whose entire branch should be skipped
SKIP_MAIN_CATEGORIES = {
    "Bar & Glassware",
    "Home Essentials",
    "Health",
}

# Get all parent category URLs
parent_urls = set(
    selector.xpath(
        '//div[contains(@class, "mega-menu__content")]'
        '//li[ul]/a/@href'
    ).getall()
)
category_dict ={}
# Get links from nested category lists
categories = selector.xpath(
    '//div[contains(@class, "mega-menu__content")]'
    '//ul[contains(@class, "list-unstyled")]'
    '/li/a['
        'not(contains(@class, "mega-menu__link--see-all"))'
    ']'
)

seen = set()

for category in categories:
    name = category.xpath('normalize-space(.)').get()
    category_url = category.xpath('./@href').get()

    if not name or not category_url:
        continue

    # Skip if this URL is also a parent category
    if category_url in parent_urls:
        continue

    # Get the parent/main category of this branch
    parent_category = category.xpath(
        'normalize-space(ancestor::li[ul][1]/a[1])'
    ).get()

    # Skip the complete branch of unwanted categories
    if parent_category in SKIP_MAIN_CATEGORIES:
        continue

    category_url =  category_url

    # Remove duplicates
    if category_url in seen:
        continue
    if "/collections/" not in category_url:
      continue

    seen.add(category_url)
    category_dict[name] = category_url

category_dict

    



