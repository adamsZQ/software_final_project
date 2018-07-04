#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 下午4:31
# @Author  : zchai
import os
from flask import Flask
import json
from lucene import VERSION, initVM, Version, WhitespaceAnalyzer, QueryParser, IndexSearcher, SimpleFSDirectory, File, getVMEnv,IndexWriter,Field, Document
import uuid

from ltp_test import sentence_split, get_stop_words

app = Flask(__name__)
storeDir = 'qNa'
analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
stop_words = get_stop_words()


@app.route('/chatTeaching/<string:data>')
def chat_teaching(data):
    # 通过json获得问题和答案
    data_json = json.loads(data)
    question = data_json('question')
    answer = data_json('answer')

    # 问题分词， 答案不分词
    question = sentence_split(question)
    # answer = sentence_split(answer)

    if not os.path.exists(storeDir):
        os.mkdir(storeDir)
    store = SimpleFSDirectory(File(storeDir))
    writer = IndexWriter(store, WhitespaceAnalyzer(Version.LUCENE_CURRENT),True,
                                     IndexWriter.MaxFieldLength.LIMITED)
    writer.setMaxFieldLength(1048576)

    # 存入lucene库
    question = question.decode('utf-8').strip()
    answer = answer.decode('utf-8').strip()
    try:
        doc = Document()
        doc.add(Field("id", str(uuid.uuid1()),
                             Field.Store.YES,
                             Field.Index.NOT_ANALYZED))
        doc.add(Field("question", question,
                             Field.Store.YES,
                             Field.Index.ANALYZED))
        doc.add(Field("answer", answer,
                             Field.Store.YES,
                             Field.Index.NOT_ANALYZED))
        writer.addDocument(doc)
    except Exception, e:
        print e


@app.route('/fuzzyMatching/<string:question>')
def fuzzy_matching(question):
    # 分词
    question = sentence_split(question)

    # 构建查找器
    directory = SimpleFSDirectory(File("qNa"))
    searcher = IndexSearcher(directory, True)

    # 开始查询
    query = QueryParser(Version.LUCENE_CURRENT, "question",
                        analyzer).parse(question)
    scoreDocs = searcher.search(query, 1).scoreDocs
    if len(scoreDocs) < 1:
        return 'failure'

    doc = searcher.doc(scoreDocs[0].doc)
    reply = doc.get("answer")

    return reply


if __name__ == '__main__':
    chat_teaching('{"question":"叽里咕噜", "answer":"叽里咕噜"}')
    reply = fuzzy_matching('叽里咕噜')
    print "reply is:", reply


