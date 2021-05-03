# Scripts 
There are two scripts in this reposistory to add questions to Moodle question banks
easily.

* `moodleconvert.py` : from CSV like format to simple moodle formats
* `moodlecloze.py` : from a question template and alternative inputs in text format to moodle **cloze** format.

You can run `make` to generated XML files from sample inputs. You can use same Makefile to convert your
questions.

## `moodleconvert.py` 

This is a simple CSV like text file to moodle xml
format converter.


Simplest usage is:
`python3 moodleconvErt.py -i sample.csv -t essay -c 'my category'`
Which outputs an XML file on stdout.

Sample input formats for each supported exam type is provided:

* sample.essay
* sample.fillblanks
* sample.multichoice
* sample.shortanswer
* sample.truefalse


Also you can run `make` to see how they are converted.
`-s` can be used to change separator between question and
answer.
`-f` can be used to change separators within the answers.
Both are set to `|` by default.

`--multianswer` and `--shuffle` are only valid for
`multichoice` exam type.

Send all feature requests to onur@ceng.metu.edu.tr


```
usage: Create a moodle xml file from questions in text format
       [-h] [-s separator_character] [-f inner_seperator] -i input_file
       [-x generated_xml_file]
       [-t truefalse|multichoice|shortanswer|essay|fillblanks] -c
       import_category [--multianswer] [--shuffle]

optional arguments:
  -h, --help            show this help message and exit
  -s separator_character, --sep separator_character
  -f inner_seperator, --fieldsep inner_seperator
  -i input_file, --inpfile input_file
  -x generated_xml_file, --xmlfile generated_xml_file
  -t truefalse|multichoice|shortanswer|essay|fillblanks, 
  --type truefalse|multichoice|shortanswer|essay|fillblanks
  -c import_category, --category import_category
  --multianswer
  --shuffle
```

## `moodlecloze.py`
This is a **Moodle cloze** question generator from a template. Input file is used to generate alternative questions from same template. Depends on Python3 Jinja2 module.

Simple usage is:
`python3 moodlecloze.py -t sample.template -i sample.inp -x sample-cloze.xml -c mycategory`


`sample-cloze.template` is a sample question template all four and more underscore (i.e. `____`) character sequence are replaced by a sub-element from input from first field. All four and more plus (i.e. `++++`) character seuqnces are replaced by the following fields containing answer patterns. If answer patterns have more than element it is a multiple choice question, otherwise it is a short answer question.

`sample.cloze` is a sample input for same template.

```
Create a moodle xml file from questions in a template, and answers from a text input
       [-h] [-s question_sep_char] [-f choice_sep_char] -i input_file -t
       template_file [-x generated_xml_file] -c import_category
       [--multianswer] [--shuffle]

optional arguments:
  -h, --help            show this help message and exit
  -s question_sep_char, --sep question_sep_char
  -f choice_sep_char, --fieldsep choice_sep_char
  -i input_file, --inpfile input_file
  -t template_file, --template template_file
  -x generated_xml_file, --xmlfile generated_xml_file
  -c import_category, --category import_category
  --multianswer
  --multibox   H|V|D   layout of multiple choices (default H)
  --shuffle
```

## `codetopng.py`

This script can be imported in input generators to create images of source code.It generates a **base64** encoded image that can be included in HTML templates as:
```HTML
<img src="data:image/png;base64,++++"/><br/>
```

Assuming `++++` is replaced by image input. Sample call to `codetopng` is:

```python
import codetopng as ctp

content = ctp.codetopng('mysource.c', language='C', noise=True)
```

 * `language` selects the source language for highlighting (default `'Python'`).
 * `encode` returns a **base64** encoded image (default `True`)
 * `noise` adds gaussian noise to image to trick OCR's (default `False`)

