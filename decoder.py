#! /usr/bin/env python
# -*- coding: utf-8 -*-

## ========================================================================
## NOT SO GOOD
## ========================================================================

import re
import sys
import nltk.util

import dbutils.statistics_redis_onedb

PUNKT = r"[.]|[,]|[:]|[;]|[!]|[?]|[/]|[\\]|[(]|[)]|[@]|[$]|[%]|[-]|[\^]"
NULL_SEPARATOR = "^$"
WORD_SEPARATOR = "_"
TYPE_SEPARATOR = ":"

def build_list(str, order = None ):
    str = re.sub(PUNKT, " ", str)
    str = str.decode("utf-8").lower().encode("utf-8")
    str = re.sub("\s+", " ", str)
    return str.split();

def build_ngram(str, order):
    list = build_list(str, order)
    return nltk.util.ngrams(list, order, pad_right=True, pad_symbol=NULL_SEPARATOR)

def handle_input(list, depth):
    cur_list = list[:depth]
    if not cur_list:
        return
    if(list):
        handle_input(list[depth:], depth)

if __name__ == "__main__":
    if 1 < len(sys.argv):
        src_list = sys.argv[1:]
        src = ' '.join(src_list).decode("utf-8").lower().encode("utf-8")
        s = build_list(src)
        handle_input(s, 5)

        ngrm_src = {}
        print "Исходный текст: <<", src, ">>"

        statistics = dbutils.statistics_redis_onedb.Statistics_redis()

        print "Перевод: ",
        for i in xrange(2, 3):
           ngrm_src[i] = build_ngram(src , i)
           for ngram in ngrm_src[i]:
               phrase = statistics.convert_ngrams_en(ngram, i)
               transs = statistics.tr_en(phrase)
               print max(transs, key=operator.itemgetter(1))[0][2:].replace("_", " "),



