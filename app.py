#coding:utf-8
import grequests
from pyquery import PyQuery as pq
import requests
import re
import itertools
import json

baseURL = 'http://www.bioon.com.cn/corporation/'

def getCompanyListUrlsForOneCategory(url):
    r = requests.get(url)
    d = pq(r.text)

    m = re.search(r'page=(\d+)', d('.seasonnav ul li:last a').attr('href'))
    if m is None:
        return []

    # http://www.bioon.com.cn/corporation/list.asp?sortid=1&typeid=1&page=5
    urls = [url + '&page=' + str(i) for i in range(1, int(m.group(1)) + 1)]

    # return map(lambda response: pq(response.text)('.feature span a').map(lambda: pq(this).attr('href')), 
    #     grequests.map((grequests.get(u) for u in urls), size = 10))
    ret = []
    for response in grequests.map((grequests.get(u) for u in urls), size = 10):
        ret.extend(pq(response.text)('.feature span a').map(lambda: pq(this).attr('href')))

    return ret
        
def getCompanyCategoryList():
    d = pq(filename = './index.html')
    return d('.content .company_category').map(getSubCategoryList)

def getSubCategoryList(index, e):
    category = pq(e)
    return category.next()('li .tt a').map(lambda: baseURL + pq(this).attr('href'))


def getCompanyList(companyCategoryList):
    ret = map(getCompanyListUrlsForOneCategory, companyCategoryList)            
    return list(itertools.chain.from_iterable(ret)) # flatten the list

def getCompanyUrls():
    """ craw URLs for all companies listed on 'http://www.bioon.com.cn/corporation/'
    """
    companyCategoryList = getCompanyCategoryList()
    companyList = getCompanyList(companyCategoryList)
    # print(companyList)

    with open('companyList.json', 'w') as f:
        json.dump(companyList, f)

def getCompanyUrlsFast():        
    """ craw URLs for all companies listed on 'http://www.bioon.com.cn/corporation/'
    """
    #
    categoryFirstPageUrls = pq(filename = './index.html')('.content .company_category').map(
        lambda: pq(this).next()('li .tt a').map(
            lambda: baseURL + pq(this).attr('href')))    

    # print(list(categoryFirstPageUrls))

    #
    def getAllPageUrlsForOneCategory(categoryFirstPageUrl, res):
        m = re.search(r'page=(\d+)', pq(res.text)('.seasonnav ul li:last a').attr('href'))
        if m:
            return [categoryFirstPageUrl + '&page=' + str(i) for i in range(1, int(m.group(1)) + 1)]
        else:
            return []    

    allPageUrls = list(itertools.chain.from_iterable( # flatten [[],[],[]]
                    map(getAllPageUrlsForOneCategory, 
                        categoryFirstPageUrls, 
                        grequests.map((grequests.get(u) for u in categoryFirstPageUrls)))))
    # print(allPageUrls)

    # #
    # companyList = []
    # for res in grequests.map((grequests.get(u) for u in allPageUrls), size = 10):
    #     companyList.extend(pq(res.text)('.feature span a').map(lambda: pq(this).attr('href')))

    companyList = [pq(res.text)('.feature span a').map(lambda: pq(this).attr('href'))
                    for res in grequests.map((grequests.get(u) for u in allPageUrls), size = 10)]
    companyList = list(itertools.chain.from_iterable(companyList))

    with open('companyListFast.json', 'w') as f:
        json.dump(companyList, f)

if __name__ == "__main__":
    import time

    t1 = time.time()
    # getCompanyUrlsFast() # was 161 secs
    getCompanyUrls() #was 216 secs
    t2 = time.time()

    print(t2 - t1) 

