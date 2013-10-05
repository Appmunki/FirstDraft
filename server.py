from flask import Flask, url_for, redirect, request
import urllib
import time
import hashlib
import os
import redis
#import firstdraft
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='page.html'))

@app.route('/api', methods = ['POST'])
def api():
    url = (request.form['url'])
    return "static/"+download_image(url, str(time.time())+".png")

@app.route('/static/content/<variable>/')
def hashData(variable):
    print str(variable)
    return "<html><body><img src='img.png' width='18%' height='18%'></body></html>"


def download_image(url,name):
    image=urllib.URLopener()
    tempName = "img/"+name
    image.retrieve(url, tempName)
    imgHash = md5Checksum(tempName)
    if not os.path.exists("static/content/"+imgHash+"/img") :
        os.makedirs("static/content/"+imgHash+"/img")
    os.rename(tempName, "static/content/"+imgHash+"/img.png")
    return "../content/"+imgHash
    #firstdraft.processImage(name);


def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return str(m.hexdigest())



if __name__ == '__main__':
    app.run(debug=True, port=80,host="0.0.0.0")
