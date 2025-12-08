import scrapy
from ..items import PhoneItem


class BoulangerSpider(scrapy.Spider):
    name = "boulanger"
    allowed_domains = ["boulanger.com"]
    start_urls = [
        "https://www.boulanger.com/c/smartphone_toutes_marques"
    ]

    def parse(self, response):
        # Chaque produit
        for product in response.css("div.product-item"):
            item = PhoneItem()

            # Nom du téléphone
            item["phone_name"] = product.css("h2.product-title::text").get(default="").strip()

            # Détection basique de la marque depuis le nom
            name_lower = item["phone_name"].lower()
            if "samsung" in name_lower:
                item["brand"] = "Samsung"
            elif "apple" in name_lower or "iphone" in name_lower:
                item["brand"] = "Apple"
            elif "xiaomi" in name_lower:
                item["brand"] = "Xiaomi"
            elif "google" in name_lower:
                item["brand"] = "Google"
            else:
                item["brand"] = None

            # Nom du site
            item["website"] = "Boulanger"

            # Prix
            price = product.css("span.price::text").get()
            item["price"] = price.strip() if price else None

            item["currency"] = "EUR"

            # URL produit
            relative_url = product.css("a::attr(href)").get()
            if relative_url:
                item["product_url"] = response.urljoin(relative_url)

            # Image
            image_url = product.css("img::attr(src)").get()
            if image_url:
                item["image_url"] = response.urljoin(image_url)

            yield item

        # Pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
