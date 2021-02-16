from lxml import etree

class Lab1Pipeline:
    def __init__(self):
        self.root: etree.Element = None

    def open_spider(self, spider):
        self.root = etree.Element(spider.name)

    def close_spider(self, spider):
        with open('output/%s_output.xml' % spider.name, 'wb') as file:
            file.write(etree.tostring(self.root, encoding="UTF-8", pretty_print=True, xml_declaration=True))

    def process_item(self, item, spider):
        if spider.name == "kpi":
            page = etree.SubElement(self.root, 'page', url=item['url'])

            for text in item['text_elements']:
                etree.SubElement(page, 'fragment', type='text').text = text

            for img_src in item['image_elements']:
                etree.SubElement(page, 'fragment', type='image').text = img_src
            
        else:
            product = etree.SubElement(self.root, 'product')
            etree.SubElement(product, 'image').text = item["image"]
            etree.SubElement(product, 'description').text = item["description"]
            etree.SubElement(product, 'price').text = item["price"]

        return item
