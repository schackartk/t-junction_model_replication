.PHONY: test, badges

test:
	@src/formatters/center.sh "Running Pytest"
	coverage run -m pytest -v \
	src/t_junction_model/*.py \
	src/formatters/*.py \
	src/tests/ \
	src/*.py
	@echo ""
	@src/formatters/center.sh "Assessing Test Coverage"
	coverage report --skip-empty \
	--omit src/make_figures.py,src/formatters/formatter_class.py,src/tests/test_make_figures.py
	@src/formatters/center.sh "Running Pylint"
	pylint --rcfile setup.cfg --exit-zero \
	src/t_junction_model/*.py \
	src/formatters/*.py \
	src/*.py \
	src/tests/*.py
	@src/formatters/center.sh "Running Flake8"
	flake8 --exit-zero \
	src/t_junction_model/*.py \
	src/formatters/*.py \
	src/*.py \
	src/tests/*.py
	@echo ""
	@src/formatters/center.sh "Running MyPy"
	mypy src/t_junction_model/*.py \
	src/formatters/*.py \
	src/*.py \
	src/tests/*.py
	@echo ""
	@src/formatters/center.sh "Done, see above for test results!"

# Generate badges for README showing:
# - number of tests
# - test coverage
# - Flake8 status
badges:
	@src/formatters/center.sh "Generating Tests Badge"
	coverage run -m pytest -v \
	--junitxml=./.reports/tests/tests.xml \
	src/t_junction_model/*.py \
	src/formatters/*.py \
	src/*.py \
	src/tests/
	genbadge tests \
	-i ./.reports/tests/tests.xml \
	-o ./.reports/tests/tests_badge.svg
	@src/formatters/center.sh "Generating Test Coverage Badge"
	coverage xml \
	--skip-empty \
	-o ./.reports/coverage/coverage_all.xml
	genbadge coverage \
	-n "total coverage" \
	-i ./.reports/coverage/coverage_all.xml \
	-o ./.reports/coverage/coverage_all_badge.svg
	coverage xml \
	--skip-empty \
	--omit src/make_figures.py,src/formatters/formatter_class.py,src/tests/*.py \
	-o ./.reports/coverage/coverage_modules.xml
	genbadge coverage \
	-n "modules coverage" \
	-i ./.reports/coverage/coverage_modules.xml \
	-o ./.reports/coverage/coverage_modules_badge.svg
	@src/formatters/center.sh "Generating Flake8 Badge"
	flake8 \
	src/t_junction_model/*.py \
	src/formatters/*.py \
	src/*.py \
	src/tests/*.py \
	--exit-zero \
	--statistics \
	--tee --output-file \
	./.reports/flake8/flake8stats.txt
	genbadge flake8 \
	-i ./.reports/flake8/flake8stats.txt \
	-o ./.reports/flake8/flake8_badge.svg
	
