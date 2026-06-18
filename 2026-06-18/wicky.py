import requests

url = "https://www.whiskyshop.com/fathers-day/best-under-100"


from parsel import Selector

response = requests.get("https://www.whiskyshop.com/fathers-day/best-under-100")

selector = Selector(text=response.text)

print(selector.css("title::text").get())

print(response.status_code)
