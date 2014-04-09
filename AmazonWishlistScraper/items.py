# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AmazonwishlistItem(Item):
    # define the fields for your item here like:
    # name = Field()
    ASIN = Field()
    URL = Field()
    Title = Field()
    Type = Field()
    Other_Data = Field()
    Cheapest = Field()
    Cheapest_Condition = Field()
    Prime_Price = Field()
    Prime_Condition = Field()
    Amazon_Price = Field()
    Cheapest_Cost_Ratio = Field()
    Prime_Cost_Ratio = Field()

class AmazonWishlistEntry(Item):
    WishListID = Field()
    ASIN = Field()