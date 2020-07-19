.PHONY: all clean

all: venv/bin/activate 

init:
	pip3 install virtualenv

venv/bin/activate:
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate && pip install -r requirements.txt 

clean:
	rm -fr venv
