FILE = report
.PHONY: biblio all latex clean

all:
	$(MAKE) latex
	$(MAKE) biblio
	$(MAKE) latex
	$(MAKE) latex

latex:
	latex -interaction=nonstopmode -shell-escape $(FILE).tex
	dvips -o $(FILE).ps $(FILE).dvi
	ps2pdf $(FILE).ps

biblio: report.bib
	bibtex $(FILE).aux

clean:
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.dvi
	rm -f *.log
	rm -f *.ps
	rm -f *.pdf
	rm -f *.pyg