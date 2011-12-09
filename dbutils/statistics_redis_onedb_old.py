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
        self.server  = redis.Redis(db=stens.Statistics_ex_nosql.STATISTICS_INDEX)
    
    def flush(self):
        self.server.flush()
    
    def save(self):
        self.server.save(False)
    
    def handle(self, en, ru):
        state = True;
        state = state and self.server.zincr("%s%s"%(stens.Statistics_ex_nosql.EN2RU_PREFIX, en), ru)
        state = state and self.server.zincr("%s%s"%(stens.Statistics_ex_nosql.RU2EN_PREFIX, ru), en)
        state = state and self.server.incr("%s%s"%(stens.Statistics_ex_nosql.EN_PREFIX, en))
        state = state and self.server.incr("%s%s"%(stens.Statistics_ex_nosql.RU_PREFIX, ru))
        return state
    
if __name__ == "__main__":
    print Statistics_redis()
