# -*- coding: utf-8 -*-

import redis
import statistics_ex_nosql as stens

class Statistics_redis(stens.Statistics_ex_nosql):
    '''
        Для Redis Server 2.4.2
    '''
    
    def __init__(self):
        self.server  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_INDEX)
        
    def flush(self):
        self.server.flushdb()
        
    def save(self):
        self.server.save()
        
    def bgsave(self):
        self.server.bgsave()
        
    def handle(self, en, ru):
        state = True;
        state = state and self.server.zincrby("%s%s"%(stens.Statistics_ex_nosql.EN2RU_PREFIX, en), ru)
        state = state and self.server.zincrby("%s%s"%(stens.Statistics_ex_nosql.RU2EN_PREFIX, ru), en)
        state = state and self.server.incr("%s%s"%(stens.Statistics_ex_nosql.EN_PREFIX, en))
        state = state and self.server.incr("%s%s"%(stens.Statistics_ex_nosql.RU_PREFIX, ru))
        return state
    
    def tr_en(self, en):
        return self.server.zrange("%s%s"%(stens.Statistics_ex_nosql.EN2RU_PREFIX, en), 0, -1, withscores=True)

if __name__ == "__main__":
    print Statistics_redis()
