from playwright.sync_api import sync_playwright    # to get new cookies
import json


URL = "https://www.myntra.com/men-casual-shirts"


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()


    page.goto(
        URL,
        wait_until="domcontentloaded"
    )


    page.wait_for_timeout(5000)


    # Get cookies
    cookies = context.cookies()


    print("Total cookies:", len(cookies))


    for cookie in cookies:
        print(
            cookie["name"],
            "=",
            cookie["value"]
        )


    # Save cookies to file
    with open(
        "cookies.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cookies,
            f,
            indent=4
        )


    print("Cookies saved")


    input("Press Enter to close...")

    browser.close()
