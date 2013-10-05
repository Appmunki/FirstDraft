

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

class VisualNode(object):
    def __init__(self, parent, vtype, bbox):
        self.parent = parent
        self.visualType = vtype
        self.boundingBox = bbox

    def isRoot():
        return self.parent == None


