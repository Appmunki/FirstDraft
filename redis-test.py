import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def insertElem(a):
    counter = getCounter()
    r.put(counter+1, a);

def test():
    for x in range(0, 37):
        insertElem(x)
    print_range(0, 10);

def getCounter():
	counter = r.get('counter')
	if counter equals 'NoneType':
	    return int(counter)
	return 0


def printNewest():
    counter = getCounter()
    print print_range(counter, counter-10)

def print_range(a, b):
    result = "<html><body>"
    for x in range (a, b):
    	result+=get_html_for(x)
    return result+="</body></html>"

def get_html_for(a):
	if not a equals 'NoneType':
	    return "<img src = \""+a+"\" height=\"50px\" width=\"50px\"><div>"+a+"</div><br />"
	return ""


if __name__ == '__main__':
    test()