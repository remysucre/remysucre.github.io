all: $(patsubst %.md,%.html,$(wildcard *.md))

%.html: %.md
	pandoc $< \
	  -f markdown+inline_code_attributes \
	  -V mainfont=Verdana \
	  -V maxwidth=750px \
	  -t html --mathml -s \
	  --highlight-style=monochrome \
	  -o $@

.PHONY: all
