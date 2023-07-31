all: blog index.html

index.html: index.md
	pandoc $< \
	  -o $@ \
	  -f markdown \
	  -t html -s \
	  -V mainfont=Verdana \
	  -V maxwidth=650px \
	  -V linestretch=1.6

blog:
	$(MAKE) -C blog

.PHONY: all blog
