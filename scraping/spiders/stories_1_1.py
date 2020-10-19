import scrapy

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Stories_1_1'  # name_gender_type
    allowed_domains = ['www.stories.com']
    start_urls = [
        'https://www.stories.com/en/clothing/whats-new.html',
        'https://www.stories.com/en/clothing/whats-new/_jcr_content/subdepartmentPar/productlisting_223e.products.html?start=20',
    ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest'
        }

        for url in self.start_urls:
            yield scrapy.http.Request(url, headers=headers, dont_filter=True)

    def parse(self, response, **kwargs):
        products = response.css('div.producttile-wrapper')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.product-title > p::text').get().strip()
            item['price'] = product.css('.m-product-price > span::text').get().strip()
            image_url = product.css('img::attr(src)').get()
            # item['image_urls'] = [image_url, image_url]
            item['product_link'] = product.css('a.a-link::attr(href)').get()
            yield item

