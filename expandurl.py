#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys
import getopt
import urllib2

expand_api_url = "http://expandurl.appspot.com/expand?url="


def get_url(argv):
    url = ""
    short_message = "usage: expandurl.py -u <URL>, type -h or --help for more information."
    full_message = "Reveal full url form its shorten form made by t.com etc.\n\n\
    \roptions:\n\
    \r  -h, --help        Display this message\n\
    \r  -u, --url <URL>   Show target url"
    try:
        opts, args = getopt.getopt(argv, "hu:", ["help", "url="])
    except getopt.GetoptError:
        print short_message
        sys.exit(2)
    if len(opts) == 0:
        print short_message
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print full_message
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
        if result["redirects"] == 0:
            print "{0} is already a full form or url".format(short_url)
        elif result["redirects"] == 1:
            print "Your url {0} refers to {1}".format(short_url, result['end_url'])
        else:
            length = result["redirects"] - 1  # 2 redirects mean there is 3 url in "urls" and we don't need
                                              # the first and the last ones
            string_to_format = "\n  * ".join(["{" + str(n) + "}" for n in range(length)])
            redirections = "  * " + string_to_format.format(*result["urls"][1:-1])
            print "Your url {0} refers to {1} through {2} jumps (redirections)\
            which are: \n{3}:".format(short_url, result['end_url'], result["redirects"], redirections)
    elif result["status"] == "TooManyRedirects":
        print "There is too may redirects (more than 10) so target url is not safe to reach"
    elif result["status"] == "InvalidURL":
        print "URL is invalid, check it and try again"
    elif result["status"] == "InternalError":
        print "Internal Error occurred, sorry, no more useful information, may be try later? "
    else:
        print "Something went wrong, url cannot be revealed"