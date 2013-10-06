import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def insertElem(a):
    counter = getCounter()
    r.delete('counter')
    r.set('counter', counter+1)
    r.set(counter, a);

def test():
    r.delete('counter')
    for x in range(0, 37):
        insertElem(x)
    print printNewest(10)

def getCounter():
	counter = r.get('counter')
	if counter:
	    return int(counter)
	return 0

def printNewest(anum):
    counter = getCounter()
    return print_range(counter-1-anum, counter-1)
 

def print_range(a, b):
    result = "<html><body>"
    for x in range (a, b):
    	temp=get_html_for(r.get(x))
	result+=temp
    result+="</body></html>"
    return result

def get_html_for(a):
	if a:
	    return "<img src = \""+a+"\" height=\"50px\" width=\"50px\"><div>"+a+"</div><br />"
	return ""


if __name__ == '__main__':
    test()
