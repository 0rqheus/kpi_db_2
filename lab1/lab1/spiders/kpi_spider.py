from scrapy.http.response import Response
import scrapy


class KpiSpider(scrapy.Spider):
    name = 'kpi'
    allowed_domains = ['kpi.ua']
    start_urls = ['https://kpi.ua']

    def parse(self, response: Response):
        image_elements = response.xpath("//img/@src")
        text_elements = response.xpath("//*[not(self::script)][not(self::style)][not(self::title)][string-length(normalize-space(text())) > 0]/text()")
        yield {
            'url': response.url,
            'text_elements': map(lambda text: text.get().strip(), text_elements),
            'image_elements': map(lambda image: 'https://kpi.ua' + image.get() if image.get().startswith('/') else image.get(), image_elements)
        }

        if response.url == self.start_urls[0]:
            link_elems = response.xpath(
                "//a/@href[starts-with(., 'https://kpi.ua/') or starts-with(., '/')]"
            )
            links = [
                link.get() for link in link_elems if link.get() != "/"
            ]
            for link in links[:20]:
                if link.startswith("/"):
                    link = "https://kpi.ua" + link
                yield scrapy.Request(link, self.parse)