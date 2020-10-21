import time
from shutil import which

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Old-navy_2_1'  # name_gender_type
    allowed_domains = ['oldnavy.gapcanada.ca']
    start_urls = [
        'https://oldnavy.gapcanada.ca/browse/category.do?cid=11174',
        'https://oldnavy.gapcanada.ca/browse/category.do?cid=11174#pageId=1'
    ]
    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
        'SELENIUM_DRIVER_ARGUMENTS': ['-headless'],
        # 'SELENIUM_DRIVER_ARGUMENTS': [],
        'SELENIUM_PROXY': '46.250.220.148:3128',
        'DOWNLOADER_MIDDLEWARES': {
            'scraping.spiders.middlewares.SeleniumMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'scraping.spiders.pipelines.ProductPipeline': 300,
            'scraping.spiders.pipelines.ImagesWithSeleniumProxyPipeline': 2,
        }
    }

    def parse(self, response, **kwargs):
        products = response.css('.product-card')
        for product in products:
            title = product.css('.product-card__name::text').get()
            price = product.css('span.product-price__no-strike::text').get()
            image_url = product.css('img::attr(src)').get()
            product_link = product.css('.product-card__link::attr(href)').get()

            if title and price and image_url and product_link:
                item = ProductItem()
                item['title'] = title
                item['price'] = price
                item['image_urls'] = [image_url, image_url]
                item['product_link'] = product_link
                yield item
