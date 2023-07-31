all: $(patsubst %.md,%.html,$(wildcard *.md))

%.html: %.md
	pandoc $< \
	  -o $@ \
	  -f markdown+inline_code_attributes \
	  -t html --mathml -s \
	  -V mainfont=Verdana \
	  -V maxwidth=750px \
	  -V linestretch=1.6 \
	  --highlight-style=monochrome

.PHONY: all
