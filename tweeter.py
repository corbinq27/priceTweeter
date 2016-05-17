__author__ = 'corbinq27'

from twython import Twython
import json
from main import CreateData
from product_extractor import ProductExtractor
from pyshorteners import Shortener
import time
import requests
from s3_file_download import FileDownload
from s3_file_upload import FileUpload

tweeter_keys = {}

def lambda_handler(event, context):


    with open("twitter_keys.json", "rb") as fp:
        tweeter_keys = json.load(fp)

    twitter = Twython(tweeter_keys["APP_KEY"], tweeter_keys["APP_SECRET"], tweeter_keys["OAUTH_TOKEN"],
                        tweeter_keys["OAUTH_TOKEN_SECRET"])

    fdownload = FileDownload()
    fdownload.file_download()

    pe = ProductExtractor()
    pe.product_extractor()

    cd = CreateData()
    new_data_filename = cd.create_data()



    fupload = FileUpload()
    if new_data_filename:
        fupload.file_upload([new_data_filename])
    else:
        fupload.file_upload()

    price_comparison = {}

    with open("/tmp/price-comparison-recent.json", "rb") as fp:
        price_comparison = json.load(fp)

    #if any price comparisons have changed (as noted in their data) then we'll tweet the product and how it changed.

    if price_comparison:
        for product, info in price_comparison.iteritems():
            short_url_obtained = False

            try:
                shortener = Shortener('Google', api_key = tweeter_keys["GOOGLE_URL_SHORTENER_KEY"])
                short_url = shortener.short(info["product_url"])
                short_url_obtained = True
            except(requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                time.sleep(2)
                if not short_url_obtained:
                    short_url = "http://goo.gl/p7KqbO" #hardcoded to wholesalegaming.biz

            if info["is_discontinued_product"] and (info["old_price"] not in "N/A"):
                #only tweet out if the old_price of a product is N/A.
                #deals with issue of the discontinued product not getting removed
                #from scraped site.
                twitter.update_status(status="%s no longer for sale. %s" % (product, short_url))
            elif info["is_new_product"]:
                twitter.update_status(status="%s now available! $%s. %s" % (product, int(info["new_price"]), short_url))
            elif info["is_difference"]:
                twitter.update_status(status='New price for %s: $%s. Was $%s. %s' % (product, int(info["new_price"]),
                                                                                     int(info["old_price"]), short_url))
            else:
                print("no change for %s" % product)
                try:
                    print('test printout for %s: $%s. Was $%s. %s' % (product, int(info["new_price"]),
                                                                                     int(info["old_price"]), short_url))
                except(ValueError):
                    #deal with the N/A price.
                    print("test printout for %s: %s. Was %s. %s" % (product, info["new_price"],
                                                                                     info["old_price"], short_url))
