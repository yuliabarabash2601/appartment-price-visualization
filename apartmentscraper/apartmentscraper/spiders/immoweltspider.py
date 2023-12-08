from urllib.parse import urlparse, parse_qs

import scrapy

class ImmoweltspiderSpider(scrapy.Spider):
    name = "immoweltspider"
    allowed_domains = ["immowelt.de"]
    start_urls = ["https://www.immowelt.de/suche/muenchen/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp=1"]

    URL_TEMPLATE = "https://www.immowelt.de/suche/muenchen/wohnungen/mieten?d=true&sd=DESC&sf=RELEVANCE&sp={page_number}"

    def parse(self, response):
        # Existing parsing logic
        estate_items = response.xpath('//div[contains(@class, "EstateItem-4409d")]')

        if not estate_items:
            return

        for estate_item in estate_items:
            name = estate_item.xpath('.//div/h2/text()').get()
            price = estate_item.xpath('.//div[@data-test="price"]/text()').get()
            size = estate_item.xpath('.//div[@data-test="area"]/text()').get()
            rooms = estate_item.xpath('.//div[@data-test="rooms"]/text()').get()

            # Process the extracted data (e.g., save it or print it)
            yield {
                'name': name,
                'price': price,
                'size': size,
                'rooms': rooms
            }

        # # Logic to generate next page URL
        current_page_url = response.url
        url_components = urlparse(current_page_url)
        query_params = parse_qs(url_components.query)

        current_page_number = int(query_params.get('sp', [1])[0])
        next_page_number = current_page_number + 1

        next_page_url = self.URL_TEMPLATE.format(page_number=next_page_number)
        return scrapy.Request(next_page_url)

