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
