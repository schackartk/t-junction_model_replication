.PHONY: test, badges

test:
	@src/module/center.sh "Running Pytest"
	coverage run -m pytest -v \
	src/module/*.py \
	src/module/tests/ \
	src/*.py \
	tests/
	@echo ""
	@src/module/center.sh "Assessing Test Coverage"
	coverage report --skip-empty --omit src/make_figures.py,src/module/formatter_class.py,tests/*.py
	@src/module/center.sh "Running Pylint"
	pylint --rcfile setup.cfg --exit-zero src/module/*.py src/module/tests/*.py src/*.py tests/*.py
	@src/module/center.sh "Running Flake8"
	flake8 --exit-zero src/module/*.py src/module/tests/*.py src/*.py tests/*.py
	@echo ""
	@src/module/center.sh "Running MyPy"
	mypy src/module/*.py src/module/tests/*.py src/*.py tests/*.py
	@echo ""
	@src/module/center.sh "Done, see above for test results!"

# Generate badges for README showing:
# - number of tests
# - test coverage
# - Flake8 status
badges:
	@src/module/center.sh "Generating Tests Badge"
	coverage run -m pytest -v \
	--junitxml=./.reports/tests/tests.xml \
	src/module/*.py \
	src/module/tests/ \
	src/*.py \
	tests/
	genbadge tests \
	-i ./.reports/tests/tests.xml \
	-o ./.reports/tests/tests_badge.svg
	@src/module/center.sh "Generating Test Coverage Badge"
	coverage xml \
	--skip-empty \
	-o ./.reports/coverage/coverage_all.xml
	genbadge coverage \
	-n "total coverage" \
	-i ./.reports/coverage/coverage_all.xml \
	-o ./.reports/coverage/coverage_all_badge.svg
	coverage xml \
	--skip-empty \
	--omit src/make_figures.py,src/module/formatter_class.py,tests/*.py \
	-o ./.reports/coverage/coverage_modules.xml
	genbadge coverage \
	-n "module coverage" \
	-i ./.reports/coverage/coverage_modules.xml \
	-o ./.reports/coverage/coverage_modules_badge.svg
	@src/module/center.sh "Generating Flake8 Badge"
	flake8 \
	src/module/*.py src/module/tests/*.py src/*.py tests/*.py \
	--exit-zero \
	--statistics \
	--tee --output-file \
	./.reports/flake8/flake8stats.txt
	genbadge flake8 \
	-i ./.reports/flake8/flake8stats.txt \
	-o ./.reports/flake8/flake8_badge.svg
	
