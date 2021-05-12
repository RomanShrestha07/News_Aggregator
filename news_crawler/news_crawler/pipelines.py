# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo


class MongoPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        # db = self.conn['test_news']
        db = self.conn['news_db']
        self.collection = db['AggregatorApp_rawnews']

    def process_item(self, item, spider):
        print('---------------------------------')
        print(item)
        self.collection.insert(dict(item))
        return item
