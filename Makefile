.PHONY: test

test:
	@src/utils/center.sh "Running Pytest"
	python3 -m pytest -v \
	src/utils/*.py \
	src/*.py
	@echo ""
	@src/utils/center.sh "Running Pylint"
	pylint --rcfile setup.cfg --exit-zero src/utils/*.py
	@src/utils/center.sh "Running Flake8"
	flake8 --exit-zero src/utils/*.py src/*.py
	@echo ""
	@src/utils/center.sh "Running MyPy"
	mypy src/utils/*.py src/*.py
	@echo ""
	@src/utils/center.sh "Done, see above for test results!"
