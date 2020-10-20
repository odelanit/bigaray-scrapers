import os
from pydoc import locate

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    settings_file_path = "scraping.settings"
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    ProductSpider = locate('scraping.spiders.pullbear_2_1.ProductSpider')

    process.crawl(ProductSpider)
    process.start()
