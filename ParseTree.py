import heapq
import cgi
import HTMLParser
import matplotlib.pyplot as plt 
#import tesseract
import cv2
import cv2.cv as cv
import Image
import pyocr
import pyocr.builders
import pyocr.cuneiform

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
                   "IMAGEDIV",
                   "LIST",
                   "LISTELEMENT"])

ContourNodeToVisualType = {
    "C":"DIV",
    "T":"TEXT",
    "1":"HEADER1",
    "2":"HEADER2",
    "3":"HEADER3",
    "4":"HEADER4",
    "5":"HEADER5",
    "6":"HEADER6",
    "H":"HEADER",
    "I":"IMAGE",
    "V":"VIDEO",
    "A":"AUDIO",
    "F":"FORM",
    "L":"LABEL",
    "U":"INPUTTEXT",
    "P":"INPUTPASSWORD",
    "O":"INPUTCHECKBOX",
    "R":"INPUTRADIOBUTTON",
    "B":"BUTTON",
    "S":"BUTTONSUBMIT",
    "E":"SELECT",
    "X":"TEXTAREA",
    "M":"IMAGEDIV",
    "K":"LIST",
    "N":"LISTELEMENT"
}

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

def ContourToVisualTree(contourRoot):
    gray = cv2.cvtColor(contourRoot.img, cv2.COLOR_BGR2GRAY)
    #image_orig = contourRoot.img
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    gray=cv2.dilate(gray,kernel)
    gray=cv2.erode(gray,kernel)
    image_orig = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    h, w, c = image_orig.shape
    iplimage = cv.CreateImageHeader((w,h), cv.IPL_DEPTH_8U, c)
    cv.SetData(iplimage, image_orig.tostring(), image_orig.dtype.itemsize*c*w)
    #image_orig = cv2.threshold(image_orig, 128, 255, cv2.THRESH_BINARY)
    #pi = Image.fromarray(image_orig)
    plt.imshow(image_orig)
    plt.show()
    #image = cv2.cv.LoadImage("../testimages/testimage4-2.png", cv2.cv.CV_LOAD_IMAGE_GRAYSCALE)
    #extracted = pyocr.cuneiform.image_to_string(pi, lang='eng', builder=pyocr.builders.TextBuilder())
    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    api.SetVariable("tessedit_char_whitelist",''.join(ContourNodeToVisualType.keys()))
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)
    tesseract.SetCvImage(iplimage, api)
    print "Getting text"
    extracted = api.GetUTF8Text()
    print extracted
    try:
        guess_char = extracted[0].upper()
    except IndexError:
        guess_char = 'C'
    if guess_char not in ContourNodeToVisualType:
        guess_char = 'C'
    visualType = ContourNodeToVisualType[guess_char]
    bbox = RelativeBoundingBox(*contourRoot.bbox)
    thisnode = VisualNode(None, visualType, bbox)
    for cnode in contourRoot.children:
        thisnode.addNewChild(ContourToVisualTree(cnode))
    return thisnode




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
        if len(strArgs)==strNumArgs:
          return selfStr % tuple(strArgs)
        else:
          return selfStr

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
        src = "http://lorempixel.com/%s/%s/cats" % (self.boundingBox.width, self.boundingBox.height)
        return "<img src='" + src  + "' %s></img>"

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
        src = "http://lorempixel.com/%s/%s/city" % (self.boundingBox.width, self.boundingBox.height)
        return "<div style='background-image: url(\"" + src  + "\")' %s>%s</div>"

class HTMLListNode(HTMLNode):
    def strTag(self):
        return "<ul %s>%s</ul>"

class HTMLListElementNode(HTMLNode):
    def strTag(self):
        return "<li %s>Lorem Ipsum</li>"

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
    VisualType.TEXTAREA: HTMLTextAreaNode,
    VisualType.IMAGEDIV: HTMLImageDivNode,
    VisualType.LIST: HTMLListNode,
    VisualType.LISTELEMENT: HTMLListElementNode
}

