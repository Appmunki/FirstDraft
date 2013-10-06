import sys
sys.path.append("..")
from ParseTree import *
from FindContours import *
from BasicHTMLGenerator import *
from CSSHTMLGenerator import *
from BootstrapHTMLGenerator import *

def writeHTMLToFile(html,filename):
    with open(filename,"w") as f:
        f.write(html)

def FirstDraft(image, basic_html, css_html, bootstrap_html):
    cf = ContourFinder()
    contours, hir, croppedImages = cf.processImage(image)
    ct = dictParse(contours,croppedImages,hir,0)
    vn = ContourToVisualTree(ct)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(hTMLTree,BasicHTMLGenerator())
    writeHTMLToFile(html,basic_html)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(hTMLTree,CSSHTMLGenerator())
    writeHTMLToFile(html,css_html)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(hTMLTree,BootstrapHTMLGenerator())
    writeHTMLToFile(html,bootstrap_html)
