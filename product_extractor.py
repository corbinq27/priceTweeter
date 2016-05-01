__author__ = 'corbinq27'

import re
import json
import urllib2

#fairly specialized python script to extract prices from specific pages on wholesalegaming.biz

class ProductExtractor():

    def __init__(self):
        pass

    def product_extractor(self):
        the_magic_regex_string = '<tr bgcolor="#FFFFFF">\r\n  <td align="left"><font color="black" face="Arial, Helvetica"'+ \
                                     ' size="2"><a CLASS="anylink" href="([^\"]+)">([^<]+)</a></font></td>'

        list_of_urls = {}
        with open("/tmp/hills_urls.json", "rb") as urls:
            list_of_urls = json.loads(urls.read())

        dict_of_pages_to_check = {"urls": []}
        for each_page in list_of_urls["urls"]:
            response = urllib2.urlopen(each_page)
            page_source = response.read()
            m = re.finditer(the_magic_regex_string, page_source)

            for each_group in m:
                url = "%s%s" % (each_page, each_group.group(1))
                print url
                dict_of_pages_to_check["urls"].append(url)

        with open("/tmp/pages_to_check.json", "w") as fp:
            json.dump(dict_of_pages_to_check, fp, sort_keys=True, indent=4)
