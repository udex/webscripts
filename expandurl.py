#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys
import getopt
import urllib2

expand_api_url = "http://expandurl.appspot.com/expand?url="


def get_url(argv):
    url = ""
    try:
        opts, args = getopt.getopt(argv, "hu:", ["help", "url="])
    except getopt.GetoptError:
        print "usage: expandurl.py -u <URL>, type -h or --help for more information."
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help_message = "Reveal full url form its shorten form made by t.com etc.\n\n\
            \roptions:\n\
            \r  -h, --help     Display this message\n\
            \r  -u, --url <URL>  Show target url"
            print help_message
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
    return url

if __name__ == "__main__":
    short_url = get_url(sys.argv[1:])
    api_url = expand_api_url + short_url
    res_json = urllib2.urlopen(api_url).read()
    result = json.loads(res_json)
    if result["status"] == "OK":
        print result['end_url']
    elif result["status"] == "InvalidURL":
        print "URL is invalid, check it and try again"
    else:
        print "Something went wrong, url cannot be revealed"