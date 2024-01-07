start:
	python3 -m venv ./env
	. ./env/bin/activate
	pip3 install -r requirements.txt
	python3 main.py

tg:
	python3 -m venv ./env
	. ./env/bin/activate
	pip3 install -r requirements.txt
	python3 tg_main.py