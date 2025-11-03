VENV=.venv
PYTHON=${VENV}/bin/python

.PHONY: venv install run test clean

venv:
	python3 -m venv ${VENV}
	${PYTHON} -m pip install --upgrade pip setuptools wheel

install: venv
	${PYTHON} -m pip install -r requirements.txt

run: install
	FLASK_DEBUG=1 ${PYTHON} main.py

test: install
	${PYTHON} -m pytest tests -q

clean:
	rm -rf ${VENV}
