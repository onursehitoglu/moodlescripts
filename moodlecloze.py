#!/usr/local/bin/python3
import argparse
import re

import sys
from jinja2 import Template

def statefull(iobj, sep, func):
	def matcher(match):
		nonlocal count
		count += 1
		return func(count, next(st), sep, match)
	st = iter(iobj)
	count = 0
	return matcher

def fromfillers(count, ansstr, sep, match):
	return ansstr

def toquestion(count, ansstr, sep, match):
	'''convert regexp match with answer item to
       cloze question items'''
	global args

	anslist = ansstr.split(sep)
	if len(anslist) == 1:
		return '{{{}:SHORTANSWER:%100%{}}}'.format(1, anslist[0])
	else:
		corr = len(list(filter(lambda s:s.startswith('='), anslist)))
		incorr = len(anslist) - corr
		if args.multianswer:
			qtype = 'MRHS' if args.shuffle else 'MRH'
			corr  = 100  //  corr
		else:
			qtype = 'MCHS' if args.shuffle else 'MCH'
			corr = 100

		incorr = - 100 // incorr
		anslist = list(map(lambda s: '%{}%{}'.format(corr, s[1:]) if s.startswith('=') else '%{}%{}'.format(incorr,s), anslist))
		return '{{{}:{}:{}}}'.format(1, qtype,  '~'.join(anslist))
	
clozebegin = '''<?xml version="1.0" ?>
<quiz>
<question type="category">
    <category>
        <text>$course$/{0}</text>
    </category>
</question>
'''

clozetemplate ='''<question type="cloze">
     <name>
         <text>{1}</text>
     </name>
     <questiontext format="html">
         <text><![CDATA[{0}]]></text>
     </questiontext>
</question>
'''
	
	

parser = argparse.ArgumentParser("Create a moodle xml file from questions in a template, and answers from a text input")

parser.add_argument('-s', '--sep', default = '|' ,  metavar = 'question_sep_char')
parser.add_argument('-f', '--fieldsep', default = '@' ,  metavar = 'choice_sep_char')
parser.add_argument('-i', '--inpfile',  required = True, metavar = 'input_file')
parser.add_argument('-t', '--template',  required = True, metavar = 'template_file')
parser.add_argument('-x', '--xmlfile', metavar = 'generated_xml_file')
parser.add_argument('-c', '--category', required = True, metavar = 'import_category')
parser.add_argument('--multianswer',  action = 'store_true')
parser.add_argument('--shuffle',  action = 'store_true')

args = parser.parse_args()




qtext = open(args.template,"r").read()
outfile = open(args.xmlfile,"w") if args.xmlfile else sys.stdout
outfile.write(clozebegin.format(args.category))


# Open input file and 
with sys.stdin if args.inpfile == '-' else open(args.inpfile, 'r') as inp:
	while True:
		inpline = inp.readline().rstrip('\n\r')
		if inpline == '':
			break
		elif inpline[0] == '#':		# skip comments (first letter)
			continue		

		splits = inpline.split(args.sep)	
		
		questiontext = re.sub('[+]{4,}', statefull(splits[0].split(args.fieldsep), '', fromfillers), qtext)

		splits = splits[1:]

		questiontext = re.sub('_{4,}', statefull(splits, args.fieldsep, toquestion), questiontext)
		outfile.write(clozetemplate.format(questiontext, 'Q'))


outfile.write('</quiz>')
	
	
