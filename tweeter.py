__author__ = 'corbinq27'

from twython import Twython
import json
from main import CreateData
from product_extractor import ProductExtractor
from pyshorteners import Shortener

tweeter_keys = {}

with open("twitter_keys.json", "rb") as fp:
    tweeter_keys = json.load(fp)

twitter = Twython(tweeter_keys["APP_KEY"], tweeter_keys["APP_SECRET"], tweeter_keys["OAUTH_TOKEN"],
                    tweeter_keys["OAUTH_TOKEN_SECRET"])

pe = ProductExtractor()
pe.product_extractor()

cd = CreateData()
cd.create_data()

price_comparison = {}

with open("price-comparison-recent.json", "rb") as fp:
    price_comparison = json.load(fp)

#if any price comparisons have changed (as noted in their data) then we'll tweet the product and how it changed.

if price_comparison:
    for product, info in price_comparison.iteritems():
        if info["is_discontinued_product"]:
            shortener = Shortener('Google', api_key = tweeter_keys["GOOGLE_URL_SHORTENER_KEY"])
            short_url = shortener.short(info["product_url"])
            twitter.update_status(status="%s no longer for sale. %s" % (product, short_url))
        elif info["is_new_product"]:
            shortener = Shortener('Google', api_key = tweeter_keys["GOOGLE_URL_SHORTENER_KEY"])
            short_url = shortener.short(info["product_url"])
            twitter.update_status(status="%s now available! $%s. %s" % (product, int(info["new_price"]), short_url))
        elif info["is_difference"]:
            shortener = Shortener('Google', api_key = tweeter_keys["GOOGLE_URL_SHORTENER_KEY"])
            short_url = shortener.short(info["product_url"])
            twitter.update_status(status='New price for %s: $%s. Was $%s. %s' % (product, int(info["new_price"]),
                                                                                 int(info["old_price"]), short_url))
        else:
            print "no change for %s" % product
            shortener = Shortener('Google', api_key = tweeter_keys["GOOGLE_URL_SHORTENER_KEY"])
            short_url = shortener.short(info["product_url"])
            print 'test printout for %s: $%s. Was $%s. %s' % (product, int(info["new_price"]),
                                                                                 int(info["old_price"]), short_url)


