import sys
sys.path.append("..")
from ParseTree import *

class BasicHTMLGenerator(HTMLGenerator):
    def __init__(self):
        pass

    def Generate(self,htmlTree):
        body = "<body>%s</body>" % str(htmlTree)
        html = "<!DOCTYPE html><html lang='en'><head><title>A First Draft</title></head>%s</html>" % body 
        return html

