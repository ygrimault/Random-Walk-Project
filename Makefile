.PHONY: report

run:
	python3 main.py > log.txt

report: report/report.tex
	cd report && $(MAKE)

tar: report
	rm -f *.tar && tar -cvf project_RW_Pretty_Probable_Platypus.tar bandit.py check.py cmdplot.py color.py colouring.py graph.py main.py q3.py q4.py report/report.pdf
