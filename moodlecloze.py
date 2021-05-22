#!/usr/bin/python3
import argparse
import re

import sys
from jinja2 import Template

def includefiles(match):
	try:
		with open(match.group(1),"r") as inpf:
			return inpf.read()
	except Exception as e:
		sys.stderr.write("matching "+ str(match.groups())+str(e))
		return ""

def statefull(iobj, sep, func):
	def matcher(match):
		nonlocal count
		count += 1
		try:
			return func(count, next(st), sep, match)
		except StopIteration:
			print(f'No match at {count}, {sep}')
			return '????'
	st = iter(iobj)
	count = 0
	return matcher

def fromfillers(count, ansstr, sep, match):
	return ansstr

#    multiple choice (MULTICHOICE_S or MCS), represented as a dropdown menu in-line in the text,
#    multiple choice (MULTICHOICE_VS or MCVS), represented as a vertical column of radio buttons, or
#    multiple choice (MULTICHOICE_HS or MCHS), represented as a horizontal row of radio-buttons.
#    multiple choice (MULTIRESPONSE_S or MRS), represented as a vertical row of checkboxes
#    multiple choice (MULTIRESPONSE_HS or MRHS), represented as a horizontal row of checkboxes

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
		lo = '' if args.multibox == 'D' else args.multibox
		if args.multianswer:
			lo = '' if args.multibox == V else lo
			qtype = 'MR' + lo + 'S' if args.shuffle else 'MR' + lo
			corr  = 100  //  corr
		else:
			qtype = 'MC' + lo + 'S' if args.shuffle else 'MC' + lo
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
         <text><![CDATA[{0}
<script>
    window.addEventListener('load', function() {
        $('input[type="radio"]').on('mouseup', function(ev) {
            ev.target.dataset.checked = ev.target.checked ? 1 : "";
        });
        $('input[type="radio"]').click(function(ev) {
            ev.target.checked = !ev.target.dataset.checked;
        });
    })
</script>]]></text>
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
parser.add_argument('--multibox',  default = 'H', choices = ['H','V','D'])
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
		
		print(splits)
		questiontext = re.sub('[+]{4,}', statefull(splits[0].split(args.fieldsep), '', fromfillers), qtext)


		splits = splits[1:]

		questiontext = re.sub('_{4,}', statefull(splits, args.fieldsep, toquestion), questiontext)
		questiontext = re.sub('``([^`]+)``', includefiles, questiontext)
		outfile.write(clozetemplate.format(questiontext, 'Q ' + inpline[:25]))


outfile.write('</quiz>')
	
	
