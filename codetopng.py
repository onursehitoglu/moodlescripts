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

        

if __name__ == '__main__':
	f = sys.stdin if  len(sys.argv) <= 1 else open(sys.argv[1])

	sys.stdout.write(codetopng(f.read()))

