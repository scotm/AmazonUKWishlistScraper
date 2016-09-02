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

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 36000

HTTPCACHE_STORAGE = 'AmazonWishlistScraper.cache_policy.BetterFilesystemCacheStorage'
#HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.DbmCacheStorage'
HTTPCACHE_IGNORE_HTTP_CODES = [500,503]
#LOG_FILE = 'logging.txt'
HTTPCACHE_POLICY = 'AmazonWishlistScraper.cache_policy.CachePolicy'
#DOWNLOAD_DELAY = 5

FEED_EXPORTERS = {
    'csv': 'AmazonWishlistScraper.feed_exporter.CSVkwItemExporter'
}

EXPORT_FIELDS = ["Title", "Other_Data", "Type", "URL", "Amazon_Price", "Cheapest", "Cheapest_Condition", "Cheapest_Cost_Ratio", "Prime_Price", "Prime_Condition", "Prime_Cost_Ratio"]
