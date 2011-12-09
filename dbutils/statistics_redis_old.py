# -*- coding: utf-8 -*-

import redis
import statistics_ex_nosql as stens

class Statistics_redis(stens.Statistics_ex_nosql):
    '''
        Для Redis Server 1.2.1
        Быстро, при определенных настройках Redis,
        но периодически падает из-за длинных ключей
    '''
    def __init__(self):
        import redis
        self.en  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_EN_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.ru  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_RU_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.en2ru  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_EN_RU_PHRASE_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
        self.ru2en  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_RU_EN_PHRASE_DB_INDEX + stens.Statistics_ex_nosql.STATISTICS_OFFSET)
    
    def flush(self):
        self.en.flush()
        self.ru.flush()
        self.en2ru.flush()
        self.ru2en.flush()
    
    def save(self):
        self.en.save(False)
        self.ru.save(False)
        self.ru2en.save(False)
        self.en2ru.save(False)
    
    def handle(self, en, ru):
        state = True;
        state = state and self.en2ru.zincr(en, ru)
        state = state and self.ru2en.zincr(ru, en)
        state = state and self.en.incr(en)
        state = state and self.ru.incr(ru)
        return state

if __name__ == "__main__":
    print Statistics_redis()
