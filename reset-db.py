import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def test():
    r.delete('counter')
    for x in range(0, 137):
        r.delete(x);

if __name__ == '__main__':
    test()
