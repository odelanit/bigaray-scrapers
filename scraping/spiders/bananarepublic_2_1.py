import time

import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from scraping.spiders.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Banana-republic_2_1'  # name_gender_type
    allowed_domains = ['bananarepublic.gapcanada.ca']
    start_urls = [
        'https://bananarepublic.gapcanada.ca/browse/category.do?cid=13846',
        'https://bananarepublic.gapcanada.ca/browse/category.do?cid=13846#pageId=1',
        'https://bananarepublic.gapcanada.ca/browse/category.do?cid=13846#pageId=2'
    ]

    def scroll(self, browser, timeout):
        scroll_pause_time = timeout
        position = 0
        step = 300

        time.sleep(scroll_pause_time)

        while True:
            position = position + step
            browser.execute_script("window.scrollTo(0, {0});".format(position))

            time.sleep(scroll_pause_time)

            document_height = browser.execute_script("return document.body.scrollHeight")
            if document_height < position:
                break

    def parse(self, response, **kwargs):
        options = Options()
        options.headless = True
        browser = webdriver.Firefox(options=options)
        browser.implicitly_wait(30)
        browser.get(response.url)
        try:
            browser.find_element_by_css_selector('.css-1qosac6').click()
        except NoSuchElementException:
            print('No close button')
        self.scroll(browser, 1)

        scrapy_selector = Selector(text=browser.page_source)
        products = scrapy_selector.css('.product-card')
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
        browser.close()
