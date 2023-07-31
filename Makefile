all: blog index.html

index.html: index.md
	pandoc $< \
	  -f markdown \
	  -V mainfont=Verdana \
	  -V maxwidth=650px \
	  -V linestretch=1.6 \
	  -t html -s \
	  -o $@

blog:
	$(MAKE) -C blog

.PHONY: all blog
