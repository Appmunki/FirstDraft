from flask import Flask, url_for, redirect, request
import urllib
import time
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='page.html'))

@app.route('/api', methods = ['POST'])
def hello():
    url = (request.form['url'])
    download_image(url, str(time.time())+".png")
    return url

def download_image(url,name):
    print name
    image=urllib.URLopener()
    image.retrieve(url,"img/"+name)

if __name__ == '__main__':
    app.run(debug=True)