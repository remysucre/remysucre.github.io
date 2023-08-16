MARKDOWN_FILES := $(wildcard blog/*.md)
BLOG := $(patsubst %.md,%.html,$(MARKDOWN_FILES))

PANDOC_OPTIONS := -f markdown+inline_code_attributes+superscript \
                  -t html --mathml -s \
                  -V mainfont=Verdana \
                  -V maxwidth=650px \
                  -V linestretch=1.6 \
                  --highlight-style=monochrome

all: index.html projects.html $(BLOG)

index.html: index.md
	pandoc $< $(PANDOC_OPTIONS) -o $@

projects.html: projects.md
	pandoc $< $(PANDOC_OPTIONS) -o $@

blog/%.html: blog/%.md
	pandoc $< $(PANDOC_OPTIONS) -o $@

.PHONY: all
