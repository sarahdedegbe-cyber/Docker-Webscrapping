import scrapy
from comparateur_spider.items import OfferItem

class Site1Spider(scrapy.Spider):
    name = "site1"
    allowed_domains = ["exemple-site1.com"]
    start_urls = [
        "https://www.exemple-site1.com/recherche?query=cle+usb"
    ]

    def parse(self, response):
        # Exemple : sélectionner tous les produits sur la page
        for product in response.css(".product"):
            raw_name = product.css(".product-title::text").get()
            if raw_name:
                raw_name = raw_name.strip()

            price_text = product.css(".product-price::text").get()
            if price_text:
                price_text = price_text.replace("€", "").replace(",", ".").strip()
                try:
                    price = float(price_text)
                except:
                    continue
            else:
                continue

            # Création de notre item
            item = OfferItem()
            item["product_name_raw"] = raw_name
            item["product_name_normalized"] = raw_name.lower().strip()
            item["site_name"] = "Site 1"
            item["price"] = price
            item["product_url"] = response.urljoin(product.css("a::attr(href)").get())

            yield item
