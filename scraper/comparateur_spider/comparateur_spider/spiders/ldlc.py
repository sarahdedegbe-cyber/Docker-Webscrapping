import scrapy
from ..items import PhoneItem


class LdlcSpider(scrapy.Spider):
    name = "ldlc"
    allowed_domains = ["ldlc.com", "www.ldlc.com"]

    # ⚠️ Mets ici l’URL de la page liste où tu vois les <li class="pdt-item">
    start_urls = [
        "https://www.ldlc.com/telephonie/telephonie-portable/mobile-smartphone/c4416/"  # à adapter si besoin
    ]

    def parse(self, response):
        # Tous les produits de la page
        products = response.css("li.pdt-item")
        self.logger.info(f"Nombre de produits trouvés sur la page : {len(products)}")

        for product in products:
            item = PhoneItem()

            # ---------- Nom du téléphone ----------
            title = product.css("h3.title-3 a::text").get()
            if title:
                title = title.strip()
            item["phone_name"] = title

            # ---------- Marque (déduite du titre) ----------
            lower = (title or "").lower()
            if "samsung" in lower:
                item["brand"] = "Samsung"
            elif "iphone" in lower or "apple" in lower:
                item["brand"] = "Apple"
            elif "xiaomi" in lower:
                item["brand"] = "Xiaomi"
            elif "google" in lower:
                item["brand"] = "Google"
            else:
                item["brand"] = None

            # ---------- Site ----------
            item["website"] = "LDLC"

            # ---------- Prix ----------
            # On récupère tous les morceaux de texte dans le bloc prix
            # (ex: "2 479", "€", "00") puis on concatène
            price_parts = product.css("div.basket div.price div.price *::text").getall()
            price_text = "".join(price_parts).strip() if price_parts else None
            # Exemple : "2 479€00" → ton pipeline MySQL fera le nettoyage
            item["price"] = price_text
            item["currency"] = "EUR"

            # ---------- URL produit ----------
            rel_url = product.css("h3.title-3 a::attr(href)").get()
            if rel_url:
                item["product_url"] = response.urljoin(rel_url)
            else:
                item["product_url"] = response.url

            # ---------- Image ----------
            image_url = product.css("div.pic img::attr(src)").get()
            if image_url:
                item["image_url"] = response.urljoin(image_url)
            else:
                item["image_url"] = None

            yield item

        # ---------- Pagination (à faire plus tard si tu veux plusieurs pages) ----------
        # next_page = response.css("a.pagination-next::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)
