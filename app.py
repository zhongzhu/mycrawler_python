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

if __name__ == "__main__":

    companyCategoryList = getCompanyCategoryList()
    # companyCategoryList = companyCategoryList[0:1]
    # print(companyCategoryList)

    companyList = getCompanyList(companyCategoryList)
    # print(companyList)
    with open('companyList.json', 'w') as f:
        json.dump(companyList, f)


    #     # print(l.decode('UTF-8').encode('gb2312'))