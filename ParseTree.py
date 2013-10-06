import heapq
import cgi
import HTMLParser
class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

VisualType = Enum(["DIV",
                   "TEXT",
                   "HEADER1",
                   "HEADER2",
                   "HEADER3",
                   "HEADER4",
                   "HEADER5",
                   "HEADER6",
                   "HEADER",
                   "IMAGE",
                   "VIDEO",
                   "AUDIO",
                   "FORM",
                   "LABEL",
                   "INPUTTEXT",
                   "INPUTPASSWORD",
                   "INPUTCHECKBOX",
                   "INPUTRADIOBUTTON",
                   "BUTTON",
                   "BUTTONSUBMIT",
                   "SELECT",
                   "TEXTAREA",
                   "IMAGEDIV"])

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
        if vtype not in VisualType:
            raise Exception("Visual Parse Error: No such visual type %s" % vtype)
        self.visualType = vtype
        self.boundingBox = bbox
        self.children = []

    def isRoot(self):
        return self.parent == None

    def addNewChild(self, newChild):
        newChild.parent = self
        heapq.heappush(self.children, newChild)
        self.children = sorted(self.children)
        return newChild

    def addChild(self, vtype, bbox):
        child = VisualNode(self,vtype,bbox)
        heapq.heappush(self.children, child)
        self.children = sorted(self.children)
        return child

    def __lt__(self,other):
        return self.boundingBox < other.boundingBox

class HTMLNode(object):
    def __init__(self,visualNode):
        self.boundingBox = visualNode.boundingBox
        self.children = []
        self.tagAttributes = ""
        for child in visualNode.children:
            if child.visualType not in VisualToHTMLMap:
                raise Exception("HTML Parse Error: No mapping from visual type %s to html node" % child.visualType)
            htmlClass = VisualToHTMLMap[child.visualType]
            self.children.append(htmlClass(child))

    
    def strChildren(self):
        strC = ""
        for child in self.children:
            strC += str(child)
        return strC

    def strTag(self):
        return "%s"

    def __str__(self):
        strArgs = []
        strArgs.append(self.tagAttributes)
        selfStr = self.strTag()
        strNumArgs = selfStr.count("%")
        if len(self.children):
            strArgs.append(self.strChildren())
        if len(strArgs)==selfStr:
          return self.strTag() % tuple(strArgs)
        else:
          return self.strTag()

class HTMLDivNode(HTMLNode):
    def strTag(self):
        return "<div %s>%s</div>"

class HTMLTextNode(HTMLNode):
    def strTag(self):
        return "Lorem Ipsum"

class HTMLH1Node(HTMLNode):
    def strTag(self):
        return "<h1 %s>Lorem Ipsum</h1>"

class HTMLH2Node(HTMLNode):
    def strTag(self):
        return "<h2 %s>Lorem Ipsum</h2>"

class HTMLH3Node(HTMLNode):
    def strTag(self):
        return "<h3 %s>Lorem Ipsum</h3>"

class HTMLH4Node(HTMLNode):
    def strTag(self):
        return "<h4 %s>Lorem Ipsum</h4>"

class HTMLH5Node(HTMLNode):
    def strTag(self):
        return "<h5 %s>Lorem Ipsum</h5>"

class HTMLH6Node(HTMLNode):
    def strTag(self):
        return "<h6 %s>Lorem Ipsum</h6>"

class HTMLHeaderNode(HTMLNode):
    def strTag(self):
        return "<header %s>%s</header>"

class HTMLImageNode(HTMLNode):
    def strTag(self):
        src = "http://lorempixel.com/%s/%s/cats" % (self.visualNode.boundingBox.width, self.visualNode.boundingBox.height)
        return "<img src='" + src  + "' %s>%s</img>"

class HTMLVideoNode(HTMLNode):
    def strTag(self):
        src = "http://media.w3.org/2010/05/bunny/movie.ogv"
        return "<video src='" + src  + "' controls %s>%s</video>"

class HTMLAudioNode(HTMLNode):
    def strTag(self):
        src = "http://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.oga"
        return "<audio src='" + src  + "' controls %s>%s</audio>"

class HTMLFormNode(HTMLNode):
    def strTag(self):
       return "<form %s>%s</form>"

class HTMLLabelNode(HTMLNode):
    def strTag(self):
        return "<label %s>Lorem</label>"

class HTMLInputTextNode(HTMLNode):
    def strTag(self):
        return "<input type='text' %s>"

class HTMLInputPasswordNode(HTMLNode):
    def strTag(self):
        return "<input type='password' %s>"

class HTMLInputCheckboxNode(HTMLNode):
    def strTag(self):
        return "<input type='checkbox' %s>"        

class HTMLInputRadioButtonNode(HTMLNode):
    def strTag(self):
        return "<input type='radiobutton' %s>"

class HTMLButtonNode(HTMLNode):
    def strTag(self):
        return "<button type='button' %s>Click</button>"

class HTMLButtonSubmitNode(HTMLNode):
    def strTag(self):
        return "<button type='submit' value='submit' %s>Submit</button>"

class HTMLSelectNode(HTMLNode):
    def strTag(self):
        return "<select %s><option value='foo'>foo</option><option value='bar'>bar</option><option value='choo'>choo</option></select>"
        
class HTMLTextAreaNode(HTMLNode):
    def strTag(self):
        return "<textarea %s></textarea>"

class HTMLImageDivNode(HTMLNode):
    def strTag(self):
        src = "http://lorempixel.com/%s/%s/city" % (self.visualNode.boundingBox.width, self.visualNode.boundingBox.height)
        return "<div style='background-image: url(\"" + src  + "\")' %s>%s</img>"


class HTMLTree(object):
    def __init__(self,rootVisualNode):
        if rootVisualNode.visualType not in VisualToHTMLMap:
            raise Exception("HTML Parse Error: No mapping from visual type %s to html node" % rootVisualNode.visualType)
        rootHtmlClass = VisualToHTMLMap[rootVisualNode.visualType]
        self.rootBodyNode = rootHtmlClass(rootVisualNode)

    def __str__(self):
        return str(self.rootBodyNode)

class HTMLGenerator(object):
    def __init__(self):
        pass
    def Generate(self,htmlTree):
        pass

def HTMLGenerate(htmlTree, htmlGenerator):
    html = htmlGenerator.Generate(htmlTree)
    htmlParser = HTMLParser.HTMLParser()
    htmlParser.feed(html)
    htmlParser.close()
    return html

VisualToHTMLMap =  { 
    VisualType.DIV: HTMLDivNode,
    VisualType.TEXT: HTMLTextNode,
    VisualType.HEADER1: HTMLH1Node,
    VisualType.HEADER2: HTMLH2Node,
    VisualType.HEADER3: HTMLH3Node,
    VisualType.HEADER4: HTMLH4Node,
    VisualType.HEADER5: HTMLH5Node,
    VisualType.HEADER6: HTMLH6Node,
    VisualType.HEADER: HTMLHeaderNode,
    VisualType.IMAGE: HTMLImageNode,
    VisualType.VIDEO: HTMLVideoNode,
    VisualType.AUDIO: HTMLAudioNode,
    VisualType.FORM: HTMLFormNode,
    VisualType.LABEL: HTMLLabelNode,
    VisualType.INPUTTEXT: HTMLInputTextNode,
    VisualType.INPUTPASSWORD: HTMLInputPasswordNode,
    VisualType.INPUTCHECKBOX: HTMLInputCheckboxNode,
    VisualType.INPUTRADIOBUTTON: HTMLInputRadioButtonNode,
    VisualType.BUTTON: HTMLButtonNode,
    VisualType.BUTTONSUBMIT: HTMLButtonSubmitNode,
    VisualType.SELECT: HTMLSelectNode,
    VisualType.TEXTAREA: HTMLTextAreaNode
}

