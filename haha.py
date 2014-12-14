# -*- coding: utf-8 -*-

from pyquery import PyQuery as q
import requests
import json

# url = u'http://w3school.com.cn/'

# r = requests.get(url)
# r.encoding = 'gb2312'
# # get the string: 领先的 Web 技术教程 - 全部免费
# s = q(r.text)('#w3 h2').text()

# with open('haha.json', 'w') as f:
#     json.dump([s], f)


# with open('haha.json', 'w') as f:
#     json.dump([s], f)

with open('companyInfo.json', 'r') as f:
    l = json.load(f)
    s = l[0]['intro']
    print(type(s))
    print(s)