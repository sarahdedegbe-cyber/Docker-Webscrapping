import scrapy

class OfferItem(scrapy.Item):
    product_name_normalized = scrapy.Field()
    product_name_raw = scrapy.Field()
    site_name = scrapy.Field()
    price = scrapy.Field()
    product_url = scrapy.Field()
