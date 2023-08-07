import scrapy


class ImmoweltSpider(scrapy.Spider):
    NEXT_PAGE_PATTERN = 'https://www.immowelt.de/liste/muenchen/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp={}'
    name = 'immowelt'
    allowed_domains = ["www.immowelt.de"]
    start_urls = ["https://www.immowelt.de/liste/muenchen/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp=1"]

    def parse(self, response):
        apartments = response.css("div.EstateItem-1c115")

        if not apartments:
            return

        for apartment in apartments:
            url = apartment.css("a::attr(href)").get()
            yield scrapy.Request(url=url, callback=self.parse_apartment)

        # get number from response.url after sp=
        current_page = int(response.url.split("sp=")[-1])
        next_page = current_page + 1
        yield scrapy.Request(url=self.NEXT_PAGE_PATTERN.format(next_page), callback=self.parse)

    def parse_apartment(self, response):
        yield {
            "title": response.css("h1.ng-star-inserted::text").get(),
            "address": response.xpath('/html/body/app-root/div/div/div/div[2]/main/app-expose/div[3]/div[1]/sd-container/sd-row[2]/sd-col[1]/app-objectmeta/app-estate-address/div/sd-cell/sd-cell-row/sd-cell-col[2]/span[2]/text()').get(),
            "rent": response.xpath('//*[@id="aUebersicht"]/app-hardfacts/div/div/div[1]/div[1]/strong/text()').get(),
            "area": response.xpath('//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[1]/span/text()').get(),
            "rooms": response.css('//*[@id="aUebersicht"]/app-hardfacts/div/div/div[2]/div[2]/span/text()').get(),
        }