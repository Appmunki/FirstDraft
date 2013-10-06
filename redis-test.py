import redis

def test():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    k = r.get('test');
    z = int(k)
    print k
    print z



if __name__ == '__main__':
    test()