import scrapy


class CjSpider(scrapy.Spider):
    name = 'cj'
    # allowed_domains = ['caijing.com']
    start_urls = ['https://www.dyxhw.com/']

    def parse(self, response):
        typess = response.xpath('//div[@class="nav clearfix"]/a[@class="j_ch_nav _block_news_menu"]/@href').getall()
        for one_type in typess:
            # print(one_type)
            yield scrapy.Request(url=one_type, callback=self.parse_types)

    def parse_types(self, response):
        news_links = response.xpath('//ul[@class="list14 ml10"]/li/a/@href').getall()
        for news_link in news_links:
            # print(news_link)
            yield scrapy.Request(url=news_link, callback=self.parse_detial)

    def parse_detial(self, response):
        title = response.xpath('//h1[@class="title"]/text()').get()
        contents = response.xpath('//div[@class="clearfix"]/p/text()').getall()
        content = '\n'.join(x for x in contents)
        recurse = response.xpath('//div[@class="info fl"]//tr/td/text()').get().strip()
        pubtime = response.xpath('//div[@class="info fl"]//span[@class="pubTime"]/text()').get()


        item = dict()
        item['title'] = title
        item['content'] = content
        item['pubtime'] = pubtime
        yield item

        rela_article = response.xpath('//div[@class="pic-list clearfix"]//h3/a/@href').getall()
        if rela_article:
            for rela in rela_article:
                yield scrapy.Request(url=rela, callback=self.parse_detial)
