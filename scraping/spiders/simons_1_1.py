import scrapy

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Simons_1_1'  # name_gender_type
    allowed_domains = ['www.simons.ca']
    start_urls = [
        'https://www.simons.ca/fr/vetements-femme/nouveautes--new-6660',
    ]

    def parse(self, response, **kwargs):
        products = response.css('div.product_card')
        for idx, product in enumerate(products):
            print(product)
            # item = ProductItem()
            # item['title'] = product.css('.product-title > p::text').get().strip()
            # item['price'] = product.css('.m-product-price > span::text').get().strip()
            # image_url = product.css('img::attr(src)').get()
            # # item['image_urls'] = [image_url, image_url]
            # item['product_link'] = product.css('a.a-link::attr(href)').get()
            # yield item

