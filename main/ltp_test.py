#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 下午4:39
# @Author  : zchai
import urllib
import urllib2

uri_base = "http://127.0.0.1:8080/ltp"

data = {
    's': '我爱北京天安门',
    'x': 'n',
    't': 'all'}

request = urllib2.Request(uri_base)
params = urllib.urlencode(data)
response = urllib2.urlopen(request, params)
content = response.read().strip()
print content