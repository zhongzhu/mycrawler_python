#coding:utf-8
# import grequests
from pyquery import PyQuery as pq

baseURL = 'http://www.bioon.com.cn/corporation/'

def pp(l):
    # print(type(l))
    # print(l.decode('UTF-8').encode('gb2312'))
    for a in l:
        print a    

def getCompanyCategoryAndURLPairs(index, e):
    category = pq(e)
    return category.next()('li .tt a').map(
        lambda: {'category': category.text() +  ':' + pq(this).text(), 'url': baseURL + pq(this).attr('href') })

if __name__ == "__main__":

# <ul class="company_list">
# <li>
# <span class="tt"><a href="list.asp?sortid=6&typeid=21">其它</a></span>
# <span class="itm">(1565)</span>
# </li>
# </ul>
    d = pq(filename = './index.html')
    companyCategoryList = d('.content .company_category').map(getCompanyCategoryAndURLPairs)
    pp(l)
    # print(l)
    # categories = d('.content .company_category a').map(lambda: pq(this).text())
    # # pp(categories)
    # sub_categories = d('.content .company_category').parent()('.company_list li .tt a').map(
    #     lambda: (pq(this).attr('href'), pq(this).text()))
    # pp(sub_categories)




    # urls = ['http://www.bioon.com.cn/corporation/index.asp']
    # rs = (grequests.get(u) for u in urls)
    # for res in grequests.map(rs):
    #     res.encoding = 'gb2312'
        
    #     # print(res.text)
    #     # print(res.content)
    #     # t = res.content
    #     t = res.text
    #     d = PyQuery(t)
    #     l = d('.content .company_category')
    #     for k in l:
    #     	print(k)
    #     # print(l.decode('UTF-8').encode('gb2312'))