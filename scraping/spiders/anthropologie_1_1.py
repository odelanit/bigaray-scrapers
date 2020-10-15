import scrapy

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Anthropologie_1_1'  # name_gender_type
    allowed_domains = ['www.anthropologie.com']
    domain = 'https://www.anthropologie.com'
    start_urls = ['https://www.anthropologie.com/clothing-new-this-week']

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('div.c-pwa-tile-grid-inner')
            for idx, product in enumerate(products):
                item = ProductItem()
                item['title'] = product.css('.c-pwa-product-tile__heading::text').get().strip()
                item['price'] = product.css('.c-pwa-product-price__current::text').get().strip()
                image_url = product.css('img::attr(src)').get()
                if 'https:' not in image_url:
                    image_url = 'https:' + image_url
                b = image_url.split('_b?')
                hq_image_url = b[0] + "_b?$a15-pdp-detail-shot$&hei=900&qlt=80&fit=constrain"
                item['image_urls'] = [image_url, hq_image_url]
                product_link = product.css('a.c-pwa-product-tile__link::attr(href)').get()
                item['product_link'] = self.domain + product_link
                yield item
