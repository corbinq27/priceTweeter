__author__ = 'corbinq27'

import json
from time import gmtime, strftime
from scrapely import Scraper


class CreateData():

    def __init__(self):
        pass

    def create_data(self):
        training_url = "http://www.wholesalegaming.biz/startrek/trekalphastarterbox/"
        data_training = {"product": "Star Trek Alpha Unlimited Starter Box", "price": "$15.00"}

        #train scrapely
        scraper = Scraper()

        scraper.train(training_url, data_training)

        #get the URLs to check

        page_json = file("pages_to_check.json").read()

        #format (all strings in unicode) : {"urls" : [ <url1 string>, <url2 string>, ... , <urln string> ] }
        urls_to_check = json.loads(page_json)

        #get data

        #dictionary with "product name": "price"
        price_list = {}

        for each_url in urls_to_check["urls"]:
            scraped_data = scraper.scrape(each_url)
            #example of a scraped data: [{u'price': [u'&nbsp;$15.00&nbsp;'], u'product': [u'Star Trek Alpha Unlimited Starter Box']}]

            #let's sanitize the price to a float and make this a dictionary entry
            dollar_string = scraped_data[0]["price"][0].replace("&nbsp;","")
            removed_dollar_sign = dollar_string.replace("$", "")
            price_as_float = float(removed_dollar_sign)

            #get the product name by itself.
            product_name = scraped_data[0]["product"][0]

            #now add the sanitized price and product name to price list
            price_list[product_name] = [price_as_float, each_url]

        #Create a json file of the prices
        timestamp = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        with open("/tmp/prices-%s.json" % timestamp, "w") as fp:
            json.dump(price_list, fp, sort_keys=True, indent=4)

        #Compare this price list to the most "recent" price list
        recent_price_list = {}

        with open('/tmp/prices-recent.json', 'r') as fp:
            recent_price_list = json.load(fp)

        #This will be the output data of comparing the old data and new data
        #format: {
        #            "product_one_name":
        #                {
        #                     "old_price": <float>
        #                     "new_price": <float>,
        #                     "new_difference": <float of new price - old price>,
        #                     "is_difference": <boolean>,
        #                     "is_new_product": <boolean>,
        #                     "is_discontinued_product": <boolean>
        #                },
        #            "product_two_name":...
        #
        comparison_data = {}

        for old_product, old_price in recent_price_list.iteritems():
            new_difference = 0.0
            is_difference = False
            is_new_product = False
            is_discontinued_product = False
            try:
                new_price = price_list[old_product]
                new_difference = new_price[0] - old_price[0]
            except(KeyError):
                #take care of the case that old_product doesn't appear on price_list
                new_price = [0.0]
                is_discontinued_product = True

            if new_difference != 0.0:
                is_difference = True

            comparison_data[old_product] = {
                                            "old_price": old_price[0],
                                            "new_price": new_price[0],
                                            "new_difference": new_difference,
                                            "is_difference": is_difference,
                                            "is_new_product": False,
                                            "is_discontinued_product": is_discontinued_product,
                                            "product_url": old_price[1]
                                        }

        #find all items on price_list that is not in recent_price_list
        new_inventory_set = set(price_list.keys()) - set(recent_price_list.keys())
        new_inventory_list = list(new_inventory_set)

        for each_product in new_inventory_list:
            comparison_data[each_product] = { "old_price": 0.0,
                                              "new_price": price_list[each_product][0],
                                              "new_difference": price_list[each_product][0],
                                              "is_difference": True,
                                              "is_new_product": True,
                                              "is_discontinued_product": False,
                                              "product_url": price_list[each_product][1]
                                        }

        #makes it easy to find the always most recent data
        with open("/tmp/price-comparison-recent.json", "w") as fp:
            json.dump(comparison_data, fp, sort_keys=True, indent=4)

        #update the recent prices
        with open("/tmp/prices-recent.json", "w") as fp:
            json.dump(price_list, fp, sort_keys=True, indent=4)

        #Create a file to be the most recent comparison data
        timestamp = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
        if "True" in comparison_data:
            filename = "/tmp/price-comparison-%s.json"
            with open(filename, "w") as fp:
                json.dump(comparison_data, fp, sort_keys=True, indent=4)
                return filename

        return None
