# -*- coding: utf-8 -*-

import grequests
from pyquery import PyQuery as pq
import requests
import re
import itertools
import json
import time

def extractCompanyInfo(url, response):
    response.encoding = 'gb2312'
    q = pq(response.text)

    # print(type(intro))
    # print(intro)
    # print(intro.encode('gb2312'))

    return {'name': q('#wrap #head .name h1').text(),
        'intro': q('.about p').contents()[0],
        'url': url}

if __name__ == "__main__":
    t1 = time.time()

    # read the company url list 
    f = open('companyUrls.json', 'r')
    companyUrls = json.load(f)
    f.close()

    #   
    companyUrls = companyUrls[0:1]
    companyInfo = map(extractCompanyInfo, companyUrls,
        grequests.map((grequests.get(u) for u in companyUrls), size = 1))

    # save company info in file companyInfo.json
    with open('companyInfo.json', 'w') as f:
        json.dump(companyInfo, f)

    t2 = time.time()

    print(t2 - t1)