import scrapy


class ImmoweltSpider(scrapy.Spider):
    name = "immowelt"
    allowed_domains = ["www.immowelt.de"]
    start_urls = ["https://www.immowelt.de"]

    def parse(self, response):
        pass
