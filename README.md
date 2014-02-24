AmazonUKWishlistScraper
=======================

Uses scrapy to pull apart Amazon UK wishlists

This scrapy project will scrape a given Amazon UK wishlist.

# Requirements

[Python 2.6 or 2.7](http://www.python.org/)
[Scrapy](http://scrapy.org/)

# Instructions

1. Clone the repository, cd into the repository, then cd into 'AmazonWishlistScraper'.

2. To get a copy of the wishlist in CSV format, complete with the best prices for Used and New conditions,
issue the following command.

   1. scrapy crawl Amazon -t csv -o output.csv

Patches welcome.