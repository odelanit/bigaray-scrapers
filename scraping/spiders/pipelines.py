# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from io import BytesIO

from PIL import Image
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline, ImageException
from scrapy_selenium import SeleniumRequest


class ProductPipeline:
    def process_item(self, item, spider):
        return item


class CfImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield SeleniumRequest(url=image_url)

    def get_images(self, response, request, info):
        driver = response.meta['driver']
        image_src = driver.find_element_by_tag_name('img')
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(image_src.screenshot_as_png))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield path, image, buf

        for thumb_id, size in self.thumbs.items():
            thumb_path = self.thumb_path(request, thumb_id, response=response.meta['screenshot'], info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf


class ImagesWithSeleniumProxyPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield SeleniumRequest(url=image_url)

    def get_images(self, response, request, info):
        driver = response.meta['driver']
        image_src = driver.find_element_by_tag_name('img')
        path = self.file_path(request, response=response, info=info)
        orig_image = Image.open(BytesIO(image_src.screenshot_as_png))

        width, height = orig_image.size
        if width < self.min_width or height < self.min_height:
            raise ImageException("Image too small (%dx%d < %dx%d)" %
                                 (width, height, self.min_width, self.min_height))

        image, buf = self.convert_image(orig_image)
        yield path, image, buf

        for thumb_id, size in self.thumbs.items():
            thumb_path = self.thumb_path(request, thumb_id, response=response.meta['screenshot'], info=info)
            thumb_image, thumb_buf = self.convert_image(image, size)
            yield thumb_path, thumb_image, thumb_buf