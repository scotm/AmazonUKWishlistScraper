# Scrapy settings for AmazonWishlistScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'AmazonWishlistScraper'

SPIDER_MODULES = ['AmazonWishlistScraper.spiders']
NEWSPIDER_MODULE = 'AmazonWishlistScraper.spiders'
#USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1566.2 Safari/537.36'
#ITEM_PIPELINES = ['AmazonWishlistScraper.pipelines.AmazonCSVExport']

#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 600
#LOG_FILE = 'logging.txt'

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0'

FEED_EXPORTERS = {
    'csv': 'AmazonWishlistScraper.feed_exporter.CSVkwItemExporter'
}

EXPORT_FIELDS = ["Title", "Other_Data", "URL", "Amazon_Price", "Cheapest", "Cheapest_Condition", "Cheapest_Cost_Ratio", "Prime_Price", "Prime_Condition", "Prime_Cost_Ratio"]
