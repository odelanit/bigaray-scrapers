import scrapy

from scraping.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Banana-republic_1_1'  # name_gender_type
    allowed_domains = ['bananarepublic.gapcanada.ca']
    start_urls = ['https://bananarepublic.gapcanada.ca/browse/category.do?cid=48422&mlink=5151%2C14432052%2Cflyout_w_new_arrivals&clink=14432052']

    def parse(self, response, **kwargs):
        if 200 <= response.status <= 209:
            products = response.css('.product-card')
            for idx, product in enumerate(products):
                item = ProductItem()
                item['title'] = product.css('.product-card__name::text').get()
                item['price'] = product.css('.product-price__regular::text').get()

                image_url = product.css('img::attr(src)').get()
                item['image_urls'] = [image_url, image_url]

                product_link = product.css('.product-card__link::attr(href)').get()
                item['product_link'] = product_link
                yield item
