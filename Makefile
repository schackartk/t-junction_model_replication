.PHONY: test

test:
	@src/utils/center.sh "Running Pytest"
	coverage run -m pytest -v \
	src/utils/*.py \
	src/*.py
	@echo ""
	@src/utils/center.sh "Assessing Test Coverage"
	coverage report --skip-empty --omit src/make_figures.py,src/utils/formatter_class.py
	@src/utils/center.sh "Running Pylint"
	pylint --rcfile setup.cfg --exit-zero src/utils/*.py
	@src/utils/center.sh "Running Flake8"
	flake8 --exit-zero src/utils/*.py src/*.py
	@echo ""
	@src/utils/center.sh "Running MyPy"
	mypy src/utils/*.py src/*.py
	@echo ""
	@src/utils/center.sh "Done, see above for test results!"
