#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 下午4:31
# @Author  : zchai
from flask import Flask

app = Flask(__name__)


@app.route('/chatTeaching/<string:data>')
def chat_teaching(data):
    print 'aa'
    # print path
    # global path_data
    # path_data = path
    # path_json = json.loads(path_data)
    #
    # t = threading.Thread(target=data_receiver, args=path_json)
    # t.start()
    # return 'path received'
