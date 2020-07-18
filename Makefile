.PHONY: all clean

all: venv/bin/activate 

init:
	pip3 install virtualenv

venv/bin/activate:
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate && pip install PyQt5 numpy matplotlib

clean:
	rm -fr venv
