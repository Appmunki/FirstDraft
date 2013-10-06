import heapq
import cgi

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
                   "TEXTAREA"])

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

<<<<<<< HEAD
VisualToHTMLMap = {
    "CONTAINER":"div",
    "TEXT":"p",
    "IMAGE":"img",
    "VIDEO":"video",
    "AUDIO":"audio",
    "INPUT":"input",
    "PASSWORD":"input",
    "HEADER":"h5",
    "BUTTON":"button",
    "TEXTINPUT":"textarea",
=======
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
>>>>>>> 956e22ddea6b9a1f017fd59f2c1b1d63284440b2
}

class HdTMLNode(object):
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

class HTMLFormNode(HTMLNode):
    def strTag(self):
<<<<<<< HEAD
        src = "http://media.w3.org/2010/07/bunny/04-Death_Becomes_Fur.oga"
        return "<audio src='" + src  + "' controls>%s</audio>"
=======
        return "<form>%s</form>"

class HTMLLabelNode(HTMLNode):
    def strTag(self):
        return "<label>Lorem</label>"

class HTMLInputTextNode(HTMLNode):
    def strTag(self):
        return "<input type='text'>"

class HTMLInputPasswordNode(HTMLNode):
    def strTag(self):
        return "<input type='password'>"

class HTMLInputCheckboxNode(HTMLNode):
    def strTag(self):
        return "<input type='checkbox'>"        

class HTMLInputRadioButtonNode(HTMLNode):
    def strTag(self):
        return "<input type='radiobutton'>"

class HTMLButtonNode(HTMLNode):
    def strTag(self):
        return "<button type='button'>Click</button>"

class HTMLButtonSubmitNode(HTMLNode):
    def strTag(self):
        return "<button type='submit' value='submit'>Submit</button>"

class HTMLSelectNode(HTMLNode):
    def strTag(self):
        return "<select><option value='foo'>foo</option><option value='bar'>bar</option><option value='choo'>choo</option></select>"
        
class HTMLTextAreaNode(HTMLNode):
    def strTag(self):
        return "<textarea></textarea>"
>>>>>>> 956e22ddea6b9a1f017fd59f2c1b1d63284440b2
