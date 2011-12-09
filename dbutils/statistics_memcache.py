# -*- coding: utf-8 -*-

import memcache
import statistics_ex_nosql as stens

class Statistics_memcache(stens.Statistics_ex_nosql):
    '''
        Медленно
    '''
    def __init__(self, connection_string = '127.0.0.1:11211', debug=0):
        import memcache
        self.server = memcache.Client([connection_string], debug=debug);
    def flush(self):
        pass;
    def save(self):
        pass;
    def _set_cnt(self, str_key):
        if(self.server.get(str_key)):
            return self.server.incr(str_key)
        else:
            return self.server.set(str_key, "1")
            
    def handle(self, en, ru):
        state = True;
        state = state and self.server.set("%s%s"%(stens.Statistics_ex_nosql.EN2RU_PREFIX, en), ru)
        state = state and self.server.set("%s%s"%(stens.Statistics_ex_nosql.RU2EN_PREFIX, ru), en)
        state = state and self._set_cnt("%s%s%s%s"%(stens.Statistics_ex_nosql.EN2RU_CNT_PREFIX, en, stens.Statistics_ex_nosql.CNT_SEPARATOR, ru))
        state = state and self._set_cnt("%s%s%s%s"%(stens.Statistics_ex_nosql.EN2RU_CNT_PREFIX, ru, stens.Statistics_ex_nosql.CNT_SEPARATOR, en))
        state = state and self._set_cnt("%s%s"%(stens.Statistics_ex_nosql.EN_PREFIX, en))
        state = state and self._set_cnt("%s%s"%(stens.Statistics_ex_nosql.EN_PREFIX, ru))
        return state

if __name__ == "__main__":
    print Statistics_memcache()
