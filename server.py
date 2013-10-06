from flask import Flask, url_for, redirect, request
import urllib
import time
import hashlib
import os
import redis
#import firstdraft

# flash stuff
app = Flask(__name__)

# init stuff
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.delete('counter')


# this routs our index, located at /static/index.html
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

# this is the endpoint of where images are sent to
# any json doc with an element named and of type url will do
# downloads the image into /static/content/<image_hash>/img.png
# returns the path the image is located at
@app.route('/api', methods = ['POST'])
def api():
    url = (request.form['url'])
    return "static/"+download_image(url, str(time.time())+".png")


# this shows a list of elemnts from a to b
# where var1 is a and var2 is b
@app.route('/list/<variable>/<variable>')
def list(min,max):
    return print_range(min, max)

# this redirects to /list/0/10
@app.route('/list/')
def list():
    return redirect("/list/0/10")


# this gives an html page containing only the image
# DEPRECIATED
@app.route('/static/content/<variable>/')
def hashData(variable):
    print str(variable)
    return "<html><body><img src='img.png' width='18%' height='18%'></body></html>"


# this downloads the image from the url
# takes a hash, saves the image under /static/content/<hash>/img.png
# then inserts that image hash into redis with the next availible ID
def download_image(url,name):
    #download the image
    image=urllib.URLopener()
    tempName = "img/"+name
    image.retrieve(url, tempName)
    
    #hash and store
    imgHash = md5Checksum(tempName)
    insertElem(imgHash)

    #move from temp to /static/content/<hash>/img.png
    hashPath = "static/content/"+imgHash;
    if not os.path.exists(hashPath) :
        os.makedirs(hashPath)
    os.rename(tempName, hashPath+"/img.png")

    #return the path of the image
    return "../content/"+imgHash


# checksup for the image
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return str(m.hexdigest())
 

# inserts the object a into redis with the next availible ID
def insertElem(a):
    counter = getCounter()
    r.delete('counter')
    r.set('counter', counter+1)
    r.set(counter, a);


# gets the next availible index for images
def getCounter():
    counter = r.get('counter')
    if counter:
        return int(counter)
    return 0
 

#  returns html for a range of images
#  STILL NEEDS A NEXT BUTTON
def print_range(a, b):
    result = "<html><body>"
    for x in range (a, b):
        temp=get_html_for(r.get(x))
    result+=temp
    result+="</body></html>"
    return result

# gets the default row for an image as HTML
def get_html_for(a):
    if a:
        return "<img src = \"/static/content/"+a+"/img.png\" height=\"50px\" width=\"50px\"><div>"+a+"</div><br />"
    return ""











if __name__ == '__main__':
    app.run(debug=True, port=80,host="0.0.0.0")
