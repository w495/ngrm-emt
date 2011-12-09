# -*- coding: utf-8 -*-

import statistics as st

class Statistics_ex_nosql(st.Statistics):
    WORD_SEPARATOR = "_"
    TYPE_SEPARATOR = ":"
    EN_PREFIX = "en:"
    RU_PREFIX = "ru:"
    EN2RU_PREFIX = "en2ru:"
    RU2EN_PREFIX = "ru2en:"
    EN2RU_CNT_PREFIX = "en2ru.cnt:"
    RU2EN_CNT_PREFIX = "ru2en.cnt:"
    CNT_SEPARATOR = ":"

    STATISTICS_INDEX = None
    
    STATISTICS_OFFSET = 0
    STATISTICS_EN_DB_INDEX = 1
    STATISTICS_RU_DB_INDEX = 2
    STATISTICS_EN_RU_PHRASE_DB_INDEX = 3
    STATISTICS_RU_EN_PHRASE_DB_INDEX = 4

    def convert_ngrams(self, ent, rut, order):
        en = "%s%s%s"%(order, Statistics_ex_nosql.TYPE_SEPARATOR,
                       Statistics_ex_nosql.WORD_SEPARATOR.join(ent))
        ru = "%s%s%s"%(order, Statistics_ex_nosql.TYPE_SEPARATOR,
                       Statistics_ex_nosql.WORD_SEPARATOR.join(rut))
        return (en, ru)

    def convert_ngrams_ru(self, ent, order):
        return "%s%s%s"%(order, Statistics_ex_nosql.TYPE_SEPARATOR,
                         Statistics_ex_nosql.WORD_SEPARATOR.join(rut))

    def convert_ngrams_en(self, ent, order):
        return "%s%s%s"%(order, Statistics_ex_nosql.TYPE_SEPARATOR,
                         Statistics_ex_nosql.WORD_SEPARATOR.join(ent))

    def handle_ngrams(self, ent, rut, order):
        en, ru = self.convert_ngrams(ent, rut, order)
        return self.handle(en, ru)

if __name__ == "__main__":
    print Statistics_ex_nosql()