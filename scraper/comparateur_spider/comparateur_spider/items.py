import scrapy

class PhoneItem(scrapy.Item):
    phone_name = scrapy.Field()
    brand = scrapy.Field()
    website = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
