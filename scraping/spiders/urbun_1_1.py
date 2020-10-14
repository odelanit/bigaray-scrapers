import json

import scrapy

from scraping.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Urban-outfitters_1_1'  # name_gender_type
    allowed_domains = ['www.urbanoutfitters.com']
    start_urls = [
        'https://www.urbanoutfitters.com/womens-new-arrivals?page=%s' % page for page in range(1, 11)
    ]
    custom_settings = {
        "DOWNLOAD_DELAY": 20
    }
    base_url = "https://www.urbanoutfitters.com"

    def parse(self, response, **kwargs):
        products = response.css('.c-pwa-tile-grid-inner')
        for idx, product in enumerate(products):
            product_link = product.css('a.c-pwa-product-tile__link::attr(href)').get()
            if product_link:
                absolute_url = self.base_url + product_link
                yield scrapy.Request(absolute_url, callback=self.parse_product)
            else:
                continue

    def parse_product(self, response):
        item = ProductItem()
        item['title'] = response.css('.c-pwa-product-meta-heading::text').get().strip()
        item['price'] = response.css('span.c-pwa-product-price__current::text').get()
        image_url = response.css('img.c-pwa-image-viewer__img::attr(src)').get()
        if image_url:
            #     b = image_url.split('_b?')
            #     hq_image_url = b[0] + "_b?$a15-pdp-detail-shot$&hei=900&qlt=80&fit=constrain"
            item['image_urls'] = [image_url, image_url]
        yield item
