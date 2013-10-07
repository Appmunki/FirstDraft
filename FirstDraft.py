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

def FirstDraft(image, basic_html='basic.html', css_html='css.html', bootstrap_html='bss.html'):
    cf = ContourFinder()
    contours, hir, croppedImages = cf.processImage(image)
    ct = dictParse(contours,croppedImages,hir,1)
    vn = ContourToVisualTree(ct)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(ht,BasicHTMLGenerator())
    writeHTMLToFile(html,basic_html)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(ht,CSSHTMLGenerator())
    writeHTMLToFile(html,css_html)
    
    ht = HTMLTree(vn)
    html = HTMLGenerate(ht,BootstrapHTMLGenerator())
    writeHTMLToFile(html,bootstrap_html)
