from flask import Flask, url_for, redirect, request
import urllib
import time
import hashlib
import os
#import firstdraft
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='page.html'))


@app.route('/api', methods = ['POST'])
def hello():
    url = (request.form['url'])
    return download_image(url, str(time.time())+".png")


def download_image(url,name):
    image=urllib.URLopener()
    tempName = "img/"+name;
    image.retrieve(url, tempName);
    imgHash = md5Checksum(tempName);
    print os.getcwd()+"/"+tempName;
    os.rename(os.getcwd()+"/"+tempName, os.getcwd()+"/"+imgHash+"/img/"+name);

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
    app.run(debug=True)