import tempfile
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import (get_lexer_by_name,get_lexer_for_filename, get_lexer_for_mimetype)
import re
from subprocess import Popen,PIPE
import os
import sys
import base64

def codetopng(source, language='python', encode = True, noise = False):
    lexer = get_lexer_by_name(language)
    with tempfile.NamedTemporaryFile(suffix='.png') as pngfile:
        highlight(source, lexer, ImageFormatter(line_pad=10,line_number_bg=None), outfile=pngfile)
        pngfile.seek(0)
        ret =  pngfile.read()
    if noise:
        convertargs =["/usr/bin/convert", "-", "-set", "colorspace", "RGB", "-separate", "-attenuate", "0.5", 
             "+noise", "gaussian", "-combine","-"]
        noiseproc = Popen(convertargs, stdin=PIPE, stdout=PIPE)
        noiseproc.stdin.write(ret)
        noiseproc.stdin.close()
        ret = noiseproc.stdout.read()
    if not encode:
        return ret
    else:
        return re.sub('\\n','', base64.encodebytes(ret).decode())

'''
def codetopng(source, language='python', encode = True, noise = True):
    pandocargs = ["/usr/bin/pandoc", "-f", "markdown", "-t", "latex", "--listings", "-s", "--pdf-engine=xelatex", "-o" ]
    with tempfile.NamedTemporaryFile(suffix='.md') as mdfile:
        pdfname = mdfile.name[:-2] + "pdf"
        mdfile.write(markdowntemplate.format(language, source).encode())
        pandocargs.extend( (pdfname, mdfile.name) )
        mdfile.seek(0)
        sys.stderr.write(' '.join(pandocargs) + "\n")
        sp = Popen(pandocargs)
        rc = sp.wait()
        if rc != 0:
            return False

    convertargs =["/usr/bin/convert", "-density", "150", pdfname] + (
            [ "-set", "colorspace", "RGB", "-separate", "-seed", "1000", "-attenuate", "1", 
             "+noise", "gaussian", "-combine"] if noise else [])

    pngname = pdfname[:-3] + "png"
    convertargs.append(pngname)
    sys.stderr.write(' '.join(convertargs) + "\n")
    cp = Popen(convertargs)
    rc = cp.wait()
    if rc != 0:
        return False

    os.unlink(pdfname)

    with open(pngname, 'rb') as pngfile:
        ret =  pngfile.read()

    os.unlink(pngname)
    if not encode:
        return ret
    else:
        return re.sub('\\n','', base64.encodebytes(ret).decode())
'''
        

if __name__ == '__main__':
	f = sys.stdin if  len(sys.argv) <= 1 else open(sys.argv[1])

	sys.stdout.write(codetopng(f.read()))

