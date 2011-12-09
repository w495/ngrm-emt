# -*- coding: utf-8 -*-

import redis
import statistics_ex_nosql as stens
        
class Statistics_redis(stens.Statistics_ex_nosql):
    '''
        Для Redis Server 2.4.2
    '''
    def __init__(self):
        self.en  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_EN_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.ru  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_RU_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.en2ru  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_EN_RU_PHRASE_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.ru2en  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_RU_EN_PHRASE_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
    def flush(self):
        self.en.flushdb()
        self.ru.flushdb()
        self.en2ru.flushdb()
        self.ru2en.flushdb()
    def bgsave(self):
        self.en.bgsave()
        self.ru.bgsave()
        self.ru2en.bgsave()
        self.en2ru.bgsave()
        
    def save(self):
        self.en.save()
        self.ru.save()
        self.ru2en.save()
        self.en2ru.save()
        
    def handle(self, en, ru):
        state = True;
        state = state and self.en2ru.zincrby(en, ru)
        state = state and self.ru2en.zincrby(ru, en)
        state = state and self.en.incr(en)
        state = state and self.ru.incr(ru)
        return state
    
if __name__ == "__main__":
    print Statistics_redis()
