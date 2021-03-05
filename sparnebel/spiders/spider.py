import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SparnebelItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class SparnebelSpider(scrapy.Spider):
	name = 'sparnebel'
	start_urls = ['https://sparnebel.dk/Nyheder?doshow269=1']

	def parse(self, response):
		post_links = response.xpath('//a[@class="layoutbox module176_2_layoutbox3"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="PagePosition NavigateNext"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)

	def parse_post(self, response):

		date = response.xpath('//p[@class="nyheder-date2016"]/text()').get()
		title = response.xpath('//h1[@class="nyheder-title2016"]/text()').get()
		content = response.xpath('//div[@id="layout269sub1mergefield4"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SparnebelItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
