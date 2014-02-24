# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.contrib.exporter import CsvItemExporter

def remove_goop(text):
	return " ".join(text.split())

class AmazonCSVExport(CsvItemExporter):
    fields_to_export = ["Title", "URL", "Amazon_Price", "Cheapest", "Cheapest_Condition", "Cheapest_Cost_Ratio", "Prime_Price", "Prime_Condition", "Prime_Cost_Ratio"]

class AmazonwishlistscraperPipeline(object):
    def process_item(self, item, spider):
    	item["Prime_Condition"] = remove_goop(item["Prime_Condition"])
        print item.keys()

        return item