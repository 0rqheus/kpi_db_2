import json
import scrapy
from scrapy.http.response import Response
from scrapy.selector import Selector

class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    allowed_domains = ['rozetka.com.ua']
    start_urls = ['https://xl-main-api.rozetka.com.ua/v3/sections/get?front-type=xl&sectionExclusive=&sectionNowInDemand1=rank=1&sectionHotNewProducts=&sectionNowInDemand2=rank=2&lang=ua']

    def parse(self, response: Response):
        data = json.loads(response.text)

        for product in data['data']["sectionExclusive"]["goods"][:20]:
            yield {
                'image': product["images"][0]["original"],
                'description': product["title"],
                'price': str(product["price"]["current"])
            }