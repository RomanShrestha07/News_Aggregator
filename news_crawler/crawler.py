from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from news_crawler.spiders.scraper import ApNewsSpider2, GuardianSpider

process = CrawlerProcess(get_project_settings())

process = CrawlerProcess()
process.crawl(ApNewsSpider2)
process.crawl(GuardianSpider)
process.start()
