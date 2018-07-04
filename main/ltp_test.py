#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 下午4:39
# @Author  : zchai
import urllib
import urllib2
import random
import time
import sys
import re

uri_base = "http://bbd.8wss.com/ltp"


def get_stop_words():
    f = open('stopwords.txt')
    stop_words = [w.strip().decode('utf-8') for w in f.read().strip().split('\n')]
    return set(stop_words)


def punctuations_filter(sentence):
    ret = re.sub("[\.\!\?\/_\{\}\[\]\(\),$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), sentence)
    return ret.strip()


def punctuations_filter2(sentence):
    f_words = ['?', '.', '*', '&', '？', '。', '，']
    for word in f_words:
        #word = word.decode('utf-8')
        sentence = sentence.replace(word, '')

    return sentence


def LTP_dp(sentence):
    data = {'s': sentence,   'x': 'n',   't': 'dp'}

    request = urllib2.Request(uri_base)
    params = urllib.urlencode(data)
    response = urllib2.urlopen(request, params)
    content = response.read()
    # print content
    dic_data = eval(content)
    data = dic_data[0][0]

    seg_list = []
    pos_list = []
    arc_list = []
    for element in data:
        seg_list.append(element['cont'])
        pos_list.append(element['pos'])
        e_arc = str(element['parent'] + 1) + ":" + element['relate']
        arc_list.append(e_arc)

    return seg_list, pos_list, arc_list


def LTP_ne(sentence):

    data = {'s': sentence,   'x': 'n',   't': 'ner'}

    request = urllib2.Request(uri_base)
    params = urllib.urlencode(data)
    response = urllib2.urlopen(request, params)
    content = response.read()
    # print content
    dic_data = eval(content)
    data = dic_data[0][0]

    seg_list = []
    pos_list = []
    ner_list = []
    for element in data:
        seg_list.append(element['cont'])
        pos_list.append(element['pos'])
        ner_list.append(element['ne'])

    return seg_list, pos_list, ner_list


# 传入一个句子，返回一个带空格的字符串
def sentence_split(sentence):
    sentence = punctuations_filter2(sentence)
    t0 = time.time()
    print "LTP预处理开始"
    time_LTP = time.time()
    content = sentence
    seg_list, pos_list, arc_list = LTP_dp(content)
    seg_list, pos_list, ner_list = LTP_ne(content)
    seg = ' '.join(seg_list)
    pos = ' '.join(pos_list)
    arc = ' '.join(arc_list)
    ner = ' '.join(ner_list)
    print "LTP预处理用时:" + str(time.time() - time_LTP)
    print "——————————"
    print '*seg:', seg
    print '*pos:', pos
    print '*arc:', arc
    print '*ner:', ner
    print "——————————"

    return seg


if __name__ == '__main__':
    sentence_split("我觉得你说的，可能存在问题，你觉得呢？")

