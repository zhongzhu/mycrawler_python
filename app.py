#coding:utf-8
import grequests
from pyquery import PyQuery as pq
import requests
import re
import itertools
import json

baseURL = 'http://www.bioon.com.cn/corporation/'

def getAllPageUrlsForOneCategory(categoryFirstPageUrl, res):
    m = re.search(r'page=(\d+)', pq(res.text)('.seasonnav ul li:last a').attr('href'))
    if m:
        return [categoryFirstPageUrl + '&page=' + str(i) for i in range(1, int(m.group(1)) + 1)]
    else:
        return [] 

def getCompanyUrls():        
    """ craw URLs for all companies listed on 'http://www.bioon.com.cn/corporation/'
    """
    #
    categoryFirstPageUrls = pq(filename = './index.html')('.content .company_category').map(
        lambda: pq(this).next()('li .tt a').map(
            lambda: baseURL + pq(this).attr('href')))    

    #
    allPageUrls = list(itertools.chain.from_iterable( # flatten [[],[],[]]
                    map(getAllPageUrlsForOneCategory, 
                        categoryFirstPageUrls, 
                        grequests.map((grequests.get(u) for u in categoryFirstPageUrls)))))

    #
    companyUrls = list(itertools.chain.from_iterable(
        [pq(res.text)('.feature span a').map(lambda: pq(this).attr('href'))
            for res in grequests.map((grequests.get(u) for u in allPageUrls), size = 10)]))    

    # save company url list in file companyUrls.json
    with open('companyUrls.json', 'w') as f:
        json.dump(companyUrls, f)

if __name__ == "__main__":
    import time

    t1 = time.time()
    getCompanyUrls()
    t2 = time.time()

    print(t2 - t1) 

