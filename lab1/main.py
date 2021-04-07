from scrapy import cmdline
from lxml import etree

# crawl sources
# cmdline.execute("scrapy crawl kpi".split())
# cmdline.execute("scrapy crawl rozetka".split())

#task 1
print("Task #1")

with open('output/kpi_output.xml', 'rb') as file:
    root = etree.parse(file)

maxAmount = 0
pages = root.xpath('//page')

for page in pages:
    amount = page.xpath('count(./fragment[@type="text"])') 
    if amount > maxAmount:
        maxAmount = amount 

print('Max amount of text elements on page - %f\n' % maxAmount)


#task 2
print("Task #2")

transform = etree.XSLT(etree.parse('transform.xsl'))
result = transform(etree.parse('output/rozetka_output.xml'))
result.write("output/rozetka_output.xhtml", pretty_print=True, encoding="UTF-8")

print("document created")