import sys
sys.path.append("..")
from ParseTree import *

class BasicHTMLGenerator(HTMLGenerator):
    def __init__(self):
        pass

    def Generate(self,htmlTree):
        body = "<body><div style='margin: auto; border: dashed; width: %dpx; height: %dpx'>%s</div></body>" % (htmlTree.rootBodyNode.boundingBox.width, htmlTree.rootBodyNode.boundingBox.height, str(htmlTree))
        html = "<!DOCTYPE html><html lang='en'><head><title>A First Draft</title></head>%s</html>" % body 
        return html

