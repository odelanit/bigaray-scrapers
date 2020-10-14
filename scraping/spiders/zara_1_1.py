import json

import scrapy

from scraping.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Zara_1_1'  # name_gender_type
    allowed_domains = ['www.zara.com']
    start_urls = [
        'https://www.zara.com/ca/en/woman-new-in-l1180.html?v1=1549286',
    ]

    def parse(self, response, **kwargs):
        products = response.css('.product')
        for idx, product in enumerate(products):
            print(product.get())
            item = ProductItem()
            name = product.css('span.product-name::text').get()
            if name:
                item['title'] = name.strip()
            else:
                continue
            item['price'] = product.css('span.main-price::attr(data-price)').get()
            image_url = product.css('img.product-media::attr(src)').get()
            if image_url and '/w/' in image_url:
                b = image_url.split('/w/')
                c = b[1].split('/')
                d = "{0}/w/900/{1}".format(b[0], c[1])

                item['image_urls'] = [image_url, d]
            else:
                continue

            product_link = product.css('a.name::attr(href)').get()
            item['product_link'] = product_link
            yield item
