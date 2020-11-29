#!/usr/local/bin/python3
import argparse
import re

import sys
from jinja2 import Template

parser = argparse.ArgumentParser("Create a moodle xml file from questions in text format")

parser.add_argument('-s', '--sep', default = '|' ,  metavar = 'separator_character')
parser.add_argument('-f', '--fieldsep', default = '|' ,  metavar = 'inner_seperator')
parser.add_argument('-i', '--inpfile',  required = True, metavar = 'input_file')
parser.add_argument('-x', '--xmlfile', metavar = 'generated_xml_file')
parser.add_argument('-t', '--type', choices = ('truefalse','multichoice','shortanswer', 'essay', 'fillblanks'), default = 'shortanswer', metavar = 'truefalse|multichoice|shortanswer|essay|fillblanks')
parser.add_argument('-c', '--category', required = True, metavar = 'import_category')
parser.add_argument('--multianswer', action = "store_true")
parser.add_argument('--shuffle', action = "store_true")

args = parser.parse_args()



qparams = {}
qparams['category'] = args.category
qparams['questiontype'] = 'cloze' if args.type == 'fillblanks' else args.type

questions = []
currenttag = None
# Open input file and 
with sys.stdin if args.inpfile == '-' else open(args.inpfile, 'r') as inp:
	while True:
		inpline = inp.readline().rstrip('\n\r')
		if inpline == '':
			break
		elif inpline[:2] == '#@':	# skip comments (first letter)
			currenttag = None if inpline[2:] == '' else inpline[2:]
			continue
		elif inpline[0] == '#':		# skip comments (first letter)
			continue		
		
		question = {}
		splits = inpline.split(args.sep, maxsplit = 1)	
		question['text'] = splits[0]

		if currenttag:
			question['tag'] = currenttag
			question['name'] = currenttag
		
		if len(splits) == 2:
			if args.type == 'truefalse':
				if splits[1].upper() in ["TRUE","T","TR"]:
					answers = ["=true","false"]
				elif splits[1].upper() in ["FALSE","F"]:
					answers = ["true","=false"]
				else:
					sys.stderr.write("Invalid truefalse answer {} skipping question {}".format(
						splits[2], splits[0]))
					continue
			else:
				answers = splits[1].split(args.fieldsep)
		else:
			answers = []

		answerlist = []

		if args.multianswer:
			question['singlefalse'] = True
		if args.shuffle:
			question['shuffle'] = True
		(corrcount,incorrcount) = (0,0)
		for ans in answers:
			anslist = ans.split('#', maxsplit = 1)
			if args.type in ['truefalse','multichoice']:
				if anslist[0][0] == '=' :
					anscorrect = True
					anstext = anslist[0][1:]
					corrcount += 1
				else:
					anscorrect = False
					anstext = anslist[0]
					incorrcount += 1
			else:
					corrcount += 1
					anscorrect = True
					anstext = anslist[0]

			ansobj = { 'text': anstext, 'correct': anscorrect}
			if len(anslist) > 1:
				ansobj['feedback'] = anslist[1]

			answerlist.append(ansobj)

		if corrcount == 0 or incorrcount == 0:
			question['correct'] = 100		
			question['incorrect'] = 0		
		else:
			question['correct'] = 100 / corrcount
			question['incorrect'] = -100 / incorrcount

		if args.type == 'fillblanks':
			question['text'] = re.sub('_{4,}',
				'{{1:SHORTANSWER:%100%{}}}',question['text']).format(
					*[ao['text'] + ('#' + ao['feedback']
						if 'feedback' in ao else '') 
						for ao in answerlist])

			question['answers'] = []
		else:
			question['answers'] = answerlist
		questions.append(question)

qparams['questions'] = questions

with open("quiz.jinja", "r") as templ:
	template = Template(templ.read())
	outfile = open(args.xmlfile,"w") if args.xmlfile else sys.stdout
	outfile.write(template.render(qparams))
	
	
