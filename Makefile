.PHONY: test

test:
	python3 -m pytest -v \
	src/utils/*.py
	pylint --rcfile setup.cfg --exit-zero src/utils/*.py
	flake8 --exit-zero src/utils/*.py
