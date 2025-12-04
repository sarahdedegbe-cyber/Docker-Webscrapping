import scrapy
from comparateur_spider.items import OfferItem

class Site2Spider(scrapy.Spider):
    name = "site2"
    allowed_domains = ["exemple-site2.com"]
    start_urls = [
        "https://www.exemple-site2.com/search?q=cle+usb"
    ]

    def parse(self, response):
        for product in response.css(".product-item"):
            raw_name = product.css(".product-item-title::text").get()
            if raw_name:
                raw_name = raw_name.strip()

            price_text = product.css(".product-item-price::text").get()
            if price_text:
                price_text = price_text.replace("€", "").replace(",", ".").strip()
                try:
                    price = float(price_text)
                except:
                    continue
            else:
                continue

            item = OfferItem()
            item["product_name_raw"] = raw_name
            item["product_name_normalized"] = raw_name.lower().strip()
            item["site_name"] = "Site 2"
            item["price"] = price
            item["product_url"] = response.urljoin(product.css("a::attr(href)").get())

            yield item
