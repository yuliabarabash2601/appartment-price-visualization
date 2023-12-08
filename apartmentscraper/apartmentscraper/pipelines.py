# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from typing import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ApartmentscraperPipeline:
    def process_item(self, item, spider):
        print("Item", item)
        # Cleaning and converting the price
        price = float(item.get('price', '').replace('.', '').replace('€', '').strip())

        # Cleaning and converting the size
        size = float(item.get('size', '').replace('m²', '').strip())

        # Cleaning and extracting the number of rooms
        rooms = float(item.get('rooms', '').replace('Zi.', '').strip())

        # Calculating price per square meter
        price_per_sqm = price / size if size else None

        return {
            'name': item.get('name', ''),
            'price': price,
            'size': size,
            'rooms': rooms,
            'price_per_sqm': price_per_sqm
        }
