#coding:utf-8
import grequests
from pyquery import PyQuery

if __name__ == "__main__":

# <ul class="company_list">
# <li>
# <span class="tt"><a href="list.asp?sortid=6&typeid=21">其它</a></span>
# <span class="itm">(1565)</span>
# </li>
# </ul>

    urls = ['http://www.bioon.com.cn/corporation/index.asp']
    rs = (grequests.get(u) for u in urls)
    for res in grequests.map(rs):
        res.encoding = 'gb2312'
        
        # print(res.text)
        # print(res.content)
        # t = res.content
        t = res.text
        d = PyQuery(t)
        l = d('.content .company_category')
        for k in l:
        	print(k)
        # print(l.decode('UTF-8').encode('gb2312'))