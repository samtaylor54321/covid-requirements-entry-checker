install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,W main.py

format:
	black *.py

test:
	python -m pytest -vv --cov=main tests.py