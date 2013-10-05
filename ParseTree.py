import heapq
import cgi

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

VisualType = Enum(["CONTAINER",
                   "TEXT",
                   "IMAGE",
                   "VIDEO",
                   "AUDIO",
                   "INPUT",
                   "PASSWORD",
                   "HEADER",
                   "BUTTON",
                   "TEXTINPUT"])

class RelativeBoundingBox(object):
    def __init__(self,offsetX,offsetY,width,height):       
        self.offsetY = offsetY
        self.width   = width
        self.height  = height
        self.offsetX = offsetX

    def __lt__(self,other):
        return (self.offsetY,self.offsetX) < (other.offsetY,other.offsetX)

class VisualNode(object):
    def __init__(self, parent, vtype, bbox):
        self.parent = parent
        self.visualType = vtype
        self.boundingBox = bbox
        self.children = []

    def isRoot():
        return self.parent == None

    def addChild(vtype,bbox):
        child = VisualNode(self,vtype,bbox)
        heapq.heappush(self.children, child)
        self.children = sorted(self.children)

    def __lt__(self,other):
        return self.boundingBox < other.boundingBox

VisualToHTMLMap = {
    "CONTAINER":"div",
    "TEXT":"h5",
    "IMAGE":"img",
    "VIDEO":"",
    "AUDIO":,
    "INPUT":,
    "PASSWORD":,
    "HEADER":,
    "BUTTON":,
    "TEXTINPUT":,
}

class HTMLNode(object):
    def __init__(self,visualNode):
        self.children = []
        
    
    def strChildren(self):
        strC = ""
        for child in self.children:
            strC += str(child)

    def strTag(self):
        return "%s"

    def __str__(self):
        return self.strTag() % self.strChildren()

class HTMLDivNode(HTMLNode):
    def strTag(self):
        return "<div>%s</div>"

class HTMLTextNode(HTMLNode):
    def strTag(self):
        return "Lorem Ipsum"

class HTMLH1Node(HTMLNode):
    def strTag(self):
        return "<h1>Lorem Ipsum</h1>"

class HTMLH2Node(HTMLNode):
    def strTag(self):
        return "<h2>Lorem Ipsum</h2>"

class HTMLH3Node(HTMLNode):
    def strTag(self):
        return "<h3>Lorem Ipsum</h3>"

class HTMLH4Node(HTMLNode):
    def strTag(self):
        return "<h4>Lorem Ipsum</h4>"

class HTMLH5Node(HTMLNode):
    def strTag(self):
        return "<h5>Lorem Ipsum</h5>"

class HTMLH6Node(HTMLNode):
    def strTag(self):
        return "<h6>Lorem Ipsum</h6>"

class HTMLHeaderNode(HTMLNode):
    def strTag(self):
        return "<header>%s</header>"

class HTMLImageNode(HTMLNode):
    def strTag(self):
        src = "http://lorempixel.com/%s/%s/cats" % (self.visualNode.bbox.width, self.visualNode.bbox.height)
        return "<img src='" + src  + "'>%s</img>"

class HTMLVideoNode(HTMLNode):
    def strTag(self):
        src = "http://media.w3.org/2010/05/bunny/movie.ogv"
        return "<video src='" + src  + "' controls>%s</video>"

class HTMLAudioNode(HTMLNode):
    def strTag(self):
        src = "http://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.oga"
        return "<audio src='" + src  + "' controls>%s</audio>"
    
class HTMLInputNode(HTMLNode):
    def strTag(self):
        src = "http://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.oga"
        return "<audio src='" + src  + "' controls>%s</audio>"
    
