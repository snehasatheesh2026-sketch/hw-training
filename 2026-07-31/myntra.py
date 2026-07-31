import csv
import json
from playwright.sync_api import sync_playwright


START_URL = "https://www.myntra.com/men-casual-shirts"
MAX_PAGES = 6

OUTPUT_FILE = "myntra_products.csv"

BASE_URL = "https://www.myntra.com"



def crawl(page):

    products = page.locator("li.product-base")

    urls = set()

    for i in range(products.count()):

        try:

            href = products.nth(i).locator("a").first.get_attribute("href")

            if href:

                if not href.startswith("http"):
                    href = BASE_URL + "/" + href.lstrip("/")

                urls.add(href)


        except Exception as e:

            print("URL error:", e)


    return list(urls)




def get_next_page_url(page):

    try:

        next_page = page.locator(
            'link[rel="next"]'
        )


        if next_page.count():

            href = next_page.get_attribute(
                "href"
            )


            if href:

                if not href.startswith("http"):

                    href = (
                        BASE_URL
                        + "/"
                        + href.lstrip("/")
                    )


                return href


    except Exception as e:

        print(
            "Next page error:",
            e
        )


    return None





def parse(page, url):

    try:

        print("Opening product:", url)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(3000)

        product_name = ""
        brand = ""
        sku = ""
        price = ""
        mpn = ""
        availability = ""
        currency = ""
        breadcrumbs = ""
        description = ""

        size_info = ""

        rating = ""

        images = []

        colors = []

        sizes = []



        # -------------------------
        # Description
        # -------------------------
        try:

            desc = page.locator(
                "p.pdp-product-description-content"
            )

            if desc.count() > 0:

                description = desc.first.inner_text().replace("\n", " ").strip()

            size = page.locator(
              "p.pdp-sizeFitDescContent"
            )

            if size.count() > 0:

            #    size_info = size.first.inner_text().strip()

                size_info = (
                    size.first
                    .inner_text()
                    .replace("\n", " ")
                    .strip()
                )

            rating_locator = page.locator(
               "div.index-flexRow.index-averageRating span"
              )

            if rating_locator.count() > 0:
                rating = rating_locator.first.inner_text().strip()

            color_links = page.locator(
                         "div.colors-container a"
                         )
            for i in range(color_links.count()):

                color = color_links.nth(i).get_attribute("title")

                if color:

                     colors.append(color)

            colors = ",".join(colors)

            size_buttons = page.locator(
                # "button.size-buttons-size-button p.size-buttons-unified-size"
                "p.size-buttons-unified-size"
                 )
            for i in range(size_buttons.count()):

                text = size_buttons.nth(i).inner_text().strip()


                size = text.split("\n")[0].strip()


                if size:

                    sizes.append(size)

            sizes = ",".join(sizes)

            image_divs = page.locator(
                  "div.image-grid-container div.image-grid-image"
                    )
            for i in range(image_divs.count()):

                style = image_divs.nth(i).get_attribute("style")

                if style:

                    image_url = (
                              style
                                .replace('background-image: url("', "")
                                 .replace('");', "")
                                .strip()
                                )
                    images.append(image_url)


            images = ",".join(images)


            # image_divs = page.locator(
            #         "div.image-grid-image"
            #        )
            # for i in range(image_divs.count()):

            #     style = image_divs.nth(i).get_attribute("style")

            #     if style:

            #         image_url = (
            #     style
            #     .replace('background-image: url("', "")
            #     .replace('");', "")

            #     .strip()
            #      )
            #         images.append(image_url)




        except Exception:

            description = ""

            size_info = ""

            rating = ""

            images = ""

            colors = ""

            sizes = ""

        # -------------------------
        # JSON-LD
        # -------------------------

        scripts = page.locator(
            'script[type="application/ld+json"]'
        )

        print("JSON scripts:", scripts.count())

        for i in range(scripts.count()):

            try:

                json_text = scripts.nth(i).inner_text()

                data = json.loads(json_text)

            except Exception:

                continue

            if not isinstance(data, dict):

                continue

            # -------------------------
            # Product
            # -------------------------

            if data.get("@type") == "Product":

                product_name = data.get(
                    "name",
                    ""
                )

                brand_data = data.get(
                    "brand",
                    {}
                )

                if isinstance(
                    brand_data,
                    dict
                ):

                    brand = brand_data.get(
                        "name",
                        ""
                    )

                else:

                    brand = brand_data

                sku = data.get(
                    "sku",
                    ""
                )

                mpn = data.get(
                    "mpn",
                    ""
                )

                offers = data.get(
                    "offers",
                    {}
                )

                if isinstance(
                    offers,
                    dict
                ):

                    price = offers.get(
                        "price",
                        ""
                    )

                    currency = offers.get(
                        "priceCurrency",
                        ""
                    )

                    availability = offers.get(
                        "availability",
                        ""
                    )

            # -------------------------
            # Breadcrumbs
            # -------------------------

            if data.get("@type") == "BreadcrumbList":

                names = []

                for item in data.get(
                    "itemListElement",
                    []
                ):

                    try:

                        name = item.get(
                            "item",
                            {}
                        ).get(
                            "name",
                            ""
                        )

                        if name:

                            names.append(
                                name
                            )

                    except Exception:

                        pass

                breadcrumbs = " > ".join(
                    names
                )

        return {

            "product_url": url,

            "product_name": product_name,

            "brand": brand,

            "product_id": sku,

            "price": price,

            "currency": currency,

            "mpn": mpn,

            "availability": availability,

            "description": description,

            "size_info" : size_info,

            "rating": rating,

            "available_colors": colors,

            "available_size": sizes,


            "images": images,

            "breadcrumbs": breadcrumbs

        }

    except Exception as e:

        print(
            "Parse error:",
            url,
            e
        )

        return {

            "product_url": url,

            "product_name": "",

            "brand": "",

            "product_id": "",

            "price": "",

            "currency": "",

            "mpn": "",

            "availability": "",

            "description": "",

            "size_info":"",

            "rating": "",

            "available_colors": "",

            "available_size": "",

            "images":"",

            "breadcrumbs": ""

        }







with sync_playwright() as p:


    browser = p.chromium.launch(

        channel="chrome",

        headless=False

    )


    context = browser.new_context()


    page = context.new_page()



    current_url = START_URL


    seen_products = set()





    with open(

        OUTPUT_FILE,

        "w",

        newline="",

        encoding="utf-8"

    ) as file:



        writer = csv.DictWriter(

            file,

            fieldnames=[

                "product_url",

                "product_name",

                "brand",

                "product_id",

                "price",

                "currency",

                "mpn",

                "availability",

                "description",

                "size_info",

                "rating",

                "available_colors",

                "available_size",

                "images",

                
                "breadcrumbs"

            ]

        )


        writer.writeheader()





        for page_no in range(

            1,

            MAX_PAGES + 1

        ):



            print("\n====================")

            print(
                "CATEGORY PAGE:",
                page_no
            )

            print(
                current_url
            )

            print("====================")





            page.goto(

                current_url,

                wait_until="domcontentloaded",

                timeout=60000

            )



            page.wait_for_selector(

                "li.product-base",

                timeout=60000

            )



            page.wait_for_timeout(3000)





            # Find next page BEFORE product navigation

            next_url = get_next_page_url(
                page
            )


            if next_url:

                print(
                    "NEXT PAGE:",
                    next_url
                )

            else:

                print(
                    "NO NEXT PAGE"
                )





            # Crawl products

            product_urls = crawl(page)



            print(
                "Products found:",
                len(product_urls)
            )





            # Remove duplicates

            new_products = []


            for url in product_urls:

                if url not in seen_products:

                    seen_products.add(url)

                    new_products.append(url)



            print(
                "Unique products:",
                len(new_products)
            )







            # Parse products

            for index, url in enumerate(

                new_products,

                start=1

            ):


                print(

                    f"PAGE {page_no} "
                    f"PRODUCT {index}/{len(new_products)}"

                )



                data = parse(

                    page,

                    url

                )



                writer.writerow(data)

                file.flush()



                print(data)






            print(
                "COMPLETED PAGE:",
                page_no
            )





            # Go next category page

            if next_url:

                current_url = next_url

            else:

                break





    print(
        "\nCSV SAVED:",
        OUTPUT_FILE
    )


    input(
        "Press Enter to close..."
    )


    context.close()

    browser.close()