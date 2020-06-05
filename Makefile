INPUTS = $(wildcard *.essay) $(wildcard *.fillblanks) 
INPUTS += $(wildcard *.truefalse) $(wildcard *.shortanswer) 
INPUTS += $(wildcard *.multichoice)

INPUTS += $(wildcard *.cloze)

TARGETS = $(INPUTS:%.essay=%-essay.xml)
TARGETS := $(TARGETS:%.fillblanks=%-fillblanks.xml)
TARGETS := $(TARGETS:%.multichoice=%-multichoice.xml)
TARGETS := $(TARGETS:%.truefalse=%-truefalse.xml)
TARGETS := $(TARGETS:%.shortanswer=%-shortanswer.xml)
TARGETS := $(TARGETS:%.cloze=%-cloze.xml)

all: $(TARGETS)

clean:
	-rm $(TARGETS)

%-essay.xml: %.essay
	 ./moodleconvert.py -t essay -i $< -c $(<:%.essay=%) -x $@

%-truefalse.xml: %.truefalse
	 ./moodleconvert.py -t truefalse -i $< -c $(<:%.truefalse=%) -x $@

%-shortanswer.xml: %.shortanswer
	 ./moodleconvert.py -t shortanswer -i $< -c $(<:%.shortanswer=%) -x $@

%-multichoice.xml: %.multichoice
	 ./moodleconvert.py -t multichoice -i $< -c $(<:%.multichoice=%) -x $@

%-fillblanks.xml: %.fillblanks
	 ./moodleconvert.py -t fillblanks -i $< -c $(<:%.fillblanks=%) -x $@

%-cloze.xml : %-cloze.template %.cloze
	./moodlecloze.py -t $(@:%.xml=%.template) -x $@ -i $(@:%-cloze.xml=%.cloze) -c $(@:%-cloze.xml=%) --multianswer
