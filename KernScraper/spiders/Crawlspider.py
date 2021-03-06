__author__ = 'Tharun'
from scrapy.spiders import Spider
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
import os

class KernSpider(Spider):
    name = "kernspider"
    handle_httpstatus_list = [404]
    download_delay = 0.5
    OUTPUT_DIR = "Data/"
    # allowed_domains = ["kern.humdrum.org", "kern.ccarh.org"]
    start_urls = (
       'http://kern.humdrum.org/',
    )

    def parse(self, response):
        categories = response.xpath("//font[@size='+1']/text()").extract()
        section = response.xpath("//center/table")[-1]
        print categories
        tables = section.xpath(".//tr[@valign='top']")
        for idx, table in enumerate(tables[:1]):
            output_path = self.OUTPUT_DIR + categories[idx] + '/'
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            links = table.xpath(".//table//a/@href").extract()
            composers = table.xpath(".//table//a/text()").extract()
            for link, composer in zip(links, composers):
                yield Request(link, callback=self.parse_link, meta={'parent_dir':output_path + composer + '/'})

    def parse_link(self, response):
        parent_dir = response.meta['parent_dir']
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        for row in response.xpath("//tr[@valign='top']"):
            try:
                file_url = row.xpath(".//td/a/@href")[1].extract()
                # print "Scraping" + file_url
                # filename = row.xpath(".//td/a/text()")[-1].extract().replace(u'\xa0',u' ').encode('utf-8')
                filename = file_url.split('/')[-1].split('&')[1].split("=")[-1]
                yield Request(file_url, callback=self.parse_song1, meta={'path':parent_dir + filename})
            except:
                continue

    def parse_song1(self, response):
        filename = response.meta['path']
        # print "Filename "+ filename
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(response.body)
