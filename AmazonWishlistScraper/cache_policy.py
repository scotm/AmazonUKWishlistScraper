import logging
from scrapy.extensions.httpcache import DummyPolicy, FilesystemCacheStorage

class CachePolicy(DummyPolicy):

    def should_cache_response(self, response, request):
        p = "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies." in response.body
        if p:
            logging.log(logging.INFO, "Robot protection detected, not caching - %s" % response.url)
            return False
        return super(CachePolicy,self).should_cache_response(response, request)

class BetterFilesystemCacheStorage(FilesystemCacheStorage):
    def retrieve_response(self, spider, request):
        response = super(BetterFilesystemCacheStorage, self).retrieve_response(spider, request)
        if response and "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies." not in response.body:
            return response
