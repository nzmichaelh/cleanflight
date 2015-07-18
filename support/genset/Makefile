all: msp.py

msp.py: msp.h proto.tmpl.py genset.py
	python3 genset.py -t proto.tmpl.py -o $@ $<
