import re
from urlparse import urlsplit, urlunsplit

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http.request import Request

from AmazonWishlistScraper.items import AmazonwishlistItem

ASIN_extractor = re.compile(r'.*\/dp\/([^\/]+)\/.*')
getprice = re.compile('[^0-9\.]')
strip_non_price = lambda x: re.sub(r'[^0-9\.]', r'', x)

def remove_goop(text):
    return " ".join(text.split())

class AmazonSpider(BaseSpider):
    name = "Amazon"
    allowed_domains = ["amazon.co.uk"]
    visited_urls = set()


    def __init__(self, name=None, **kwargs):
        super(AmazonSpider, self).__init__(name, **kwargs)
        if 'initialpage' not in kwargs:
            self.start_urls = (
                'http://www.amazon.co.uk/registry/wishlist/2ZOJN0LT8HT1F?filter=all&reveal=unpurchased&layout=compact&sort=date-added',
            )
        else:
            p = urlsplit(kwargs['initialpage'])
            self.start_urls = (
                urlunsplit([p.scheme,p.netloc,p.path,'filter=all&reveal=unpurchased&layout=compact&sort=date-added','']),
            )

    def parse(self, response):
        hxs = Selector(response)
        if response.url in self.start_urls:
            pages = [int(re.sub('.*&page=([0-9]+).*', r'\1', x)) for x in
                     hxs.xpath('//div[@class="pagDiv"]//a/@href').extract()]
            numpages = max(pages) if pages else False
            if numpages:
                for i in range(2, numpages + 1):
                    yield self.make_requests_from_url(response.url + '&page=%d' % i)

        if response.url not in self.visited_urls:
            self.visited_urls.add(response.url)
            # Skip the first row - it's just header information
            for i in hxs.xpath('//tbody[@class="itemWrapper"]'):
                ASIN = i.xpath('./@name')[0].extract().split('.')[-1]
                request = Request('http://www.amazon.co.uk/gp/offer-listing/%s/' % ASIN, callback=self.parse_offers)
                request.meta['ASIN'] = ASIN
                amazonprice = i.xpath('.//span[@class="price"]/strong/text()').extract()
                if amazonprice:
                    request.meta["Amazon_Price"] = float(getprice.sub(r'', amazonprice[0]))
                yield request

    def parse_offers(self, response):
        hxs = Selector(response)
        ASIN = response.meta["ASIN"]
        row_xpath = '//div[@id="bucketnew"]/div/table[2]/tbody[@class="result"]/tr'
        prices = hxs.xpath("//div[contains(@class,'olpOffer')]")[1:]

        # Amazon (almost) always returns the lowest priced offer - so take the first
        item = AmazonwishlistItem()
        item["ASIN"] = ASIN
        item["URL"] = "http://www.amazon.co.uk/dp/%s/?tag=eyeforfilm-21" % ASIN
        item["Title"] = remove_goop([x for x in hxs.xpath("//div[@id='olpProductDetails']//h1/text()").extract() if x.strip()][0])
        item["Other_Data"] = remove_goop([x for x in hxs.xpath('//div[@id="olpProductByline"]/text()').extract() if x.strip()][0])
        item["Amazon_Price"] = response.meta.get('Amazon_Price', '')

        if prices:
            cheapestprice = prices[0].xpath('.//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()').extract()
            basecost = float(strip_non_price(cheapestprice[0]))
            cheapestshipping = prices[0].xpath('.//span[@class="olpShippingPrice"]/text()').extract()
            shipping = float(strip_non_price(cheapestshipping[0])) if cheapestshipping else 0.0
            item["Cheapest"] = basecost + shipping
            item["Cheapest_Condition"] = remove_goop(prices[0].xpath('.//h3/text()').extract()[0])
            if "Cheapest" in item and "Amazon_Price" in item and item["Cheapest"] and item["Amazon_Price"]:
                item["Cheapest_Cost_Ratio"] = round(float(item["Cheapest"]) / float(item["Amazon_Price"]), 3)
        free_shipping = [x for x in prices if x.xpath('.//span[@class="supersaver"]')]
        if free_shipping:
            free_shipping_price = free_shipping[0].xpath('.//span[@class="a-size-large a-color-price olpOfferPrice a-text-bold"]/text()').extract()[0]
            item["Prime_Price"] = strip_non_price(free_shipping_price)
            item["Prime_Condition"] = remove_goop(free_shipping[0].xpath('.//h3/text()').extract()[0])
            if "Prime_Price" in item and "Amazon_Price" in item and item["Prime_Price"] and item["Amazon_Price"]:
                item["Prime_Cost_Ratio"] = round(float(item["Prime_Price"]) / float(item["Amazon_Price"]),3)
            yield item
        else:
            # Create a secondary check - see if there's free shipping down the line
            request = Request('http://www.amazon.co.uk/gp/offer-listing/%s/ref=olp_prime_all?shipPromoFilter=1' % ASIN,
                              callback=self.parse_freeshipping)
            request.meta["Item"] = item
            yield request

    def parse_freeshipping(self, response):
        hxs = Selector(response)
        item = response.meta["Item"]
        row_xpath = '//div[@id="bucketnew"]/div/table[2]/tbody[@class="result"]/tr'
        free_shipping = [x for x in hxs.xpath(row_xpath) if x.xpath('.//span[@class="supersaver"]')]
        if free_shipping:
            free_shipping_price = free_shipping[0].xpath('.//span[@class="price"]/text()').extract()[0]
            item["Prime_Price"] = strip_non_price(free_shipping_price)
            item["Prime_Condition"] = free_shipping[0].xpath('.//div[@class="condition"]/text()').extract()[
                0].strip().replace('\n', '')
        yield item
