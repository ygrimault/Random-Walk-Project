.PHONY: report

run:
	python3 main.py > log.txt

report: report/report.tex
	cd report && $(MAKE)