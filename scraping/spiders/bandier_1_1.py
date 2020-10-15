import scrapy

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Bandier_1_1'  # name_gender_type
    allowed_domains = ['www.bandier.com']
    start_urls = ['https://www.bandier.com/collections/new-arrivals']

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('.js-product-container')
            for idx, product in enumerate(products):
                item = ProductItem()
                item['title'] = product.css('.js-product-item-title::text').get()
                item['price'] = product.css('.product-item__price.js-product-item-price::text').get()

                image_url = product.css('img::attr(data-src)').get()
                item['image_urls'] = [image_url, image_url]

                product_link = product.css('.image-container.js-image-container::attr(href)').get()
                item['product_link'] = product_link
                yield item
