import sys
sys.path.append("..")
from ParseTree import *

class CSSHTMLGenerator(HTMLGenerator):
    def __init__(self):
        self.cssRules = {}
        pass

    def Generate(self,htmlTree):
        self.generateCSSRules(htmlTree.rootBodyNode,"a")
        style = self.generateCSSStyle(self.cssRules)
        style = "<style type='text/css'>%s</style>" % style
        body = "<body><div style='border: dashed; width: %dpx; height: %dpx'>%s</div></body>" % (htmlTree.rootBodyNode.boundingBox.width, htmlTree.rootBodyNode.boundingBox.height, str(htmlTree))
        html = "<!DOCTYPE html><html lang='en'><head><title>A First Draft</title> %s </head>%s</html>" % (style,body)
        return html

    def generateCSSRules(self,node,node_id):
        node_id = node_id + "a"
        bbox = node.boundingBox
        rules = {}
        rules['position'] = 'absolute'
        rules['top'] = '%dpx' % bbox.offsetY
        rules['left'] = '%dpx' % bbox.offsetX
        rules['width'] = '%dpx' % bbox.width
        rules['height'] = '%dpx' % bbox.height
        self.cssRules[node_id] = rules
        node.tagAttributes = "id='%s'" % node_id
        node_id_counter = 0;
        for i,child in enumerate(node.children):
            self.generateCSSRules(child,node_id+chr(ord(node_id[-1])+node_id_counter))
            node_id_counter += 1

    def generateCSSStyle(self,rules):
        style = ""
        for nid, rl in rules.iteritems():
            style += "#%s { \n" % nid
            for prop, val in rl.iteritems():
                style += "%s: %s;\n" % (prop,val)
            style += "}\n\n"
        return style
