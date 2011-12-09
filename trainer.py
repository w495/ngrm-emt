#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xml.parsers.expat
import codecs
import re
import nltk.util

import dbutils.statistics_redis_onedb


PUNKT = r"[.]|[,]|[:]|[;]|[!]|[?]|[/]|[\\]|[(]|[)]|[@]|[$]|[%]|[-]|[\^]"
NULL_SEPARATOR = "^$"
WORD_SEPARATOR = "_"
TYPE_SEPARATOR = ":"

def train_model(order, statistics, filename):
    enfile = open("%s.en"% filename)
    rufile = open("%s.ru"% filename)
    line = 0
    file = open("temp", "w")
    while (True):
        if not (line % 1000):
            print "%s:\t%s"%(order, line)
        line +=1
        
        enstr = enfile.readline()
        rustr = rufile.readline()
        if (not enstr) or (not rustr ):
            break
        enstr = re.sub(PUNKT, " ", enstr)
        rustr = re.sub(PUNKT, " ", rustr)
        
        enstr = enstr.decode("utf-8").lower().encode("utf-8")
        rustr = rustr.decode("utf-8").lower().encode("utf-8")

        enstr = re.sub("\s+", " ", enstr)
        rustr = re.sub("\s+", " ", rustr)
        
        enstr_list = enstr.split();
        rustr_list = rustr.split();
    
        enstr_list = nltk.util.ngrams(enstr_list, order , pad_right=True, pad_symbol=NULL_SEPARATOR)
        rustr_list = nltk.util.ngrams(rustr_list, order , pad_right=True, pad_symbol=NULL_SEPARATOR)
        for (ent, rut) in zip(enstr_list, rustr_list):
            if not statistics.handle_ngrams(ent, rut, order):
                print "error"
                break;
    file.close()
    enfile.close()
    rufile.close()

if __name__ == "__main__":
    statistics = dbutils.statistics_redis_onedb.Statistics_redis()
    for i in xrange(1, 4):
        train_model(i, statistics, "uncorpora")
