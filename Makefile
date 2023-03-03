.PHONY: test, badges

test:
	@src/utils/center.sh "Running Pytest"
	coverage run -m pytest -v \
	src/t_junction_model/*.py \
	src/utils/*.py \
	src/t_junction_model/tests/ \
	src/*.py \
	tests/
	@echo ""
	@src/utils/center.sh "Assessing Test Coverage"
	coverage report --skip-empty \
	--omit src/make_figures.py,src/utils/formatter_class.py,tests/*.py
	@src/utils/center.sh "Running Pylint"
	pylint --rcfile setup.cfg --exit-zero \
	src/t_junction_model/*.py \
	src/utils/*.py \
	src/t_junction_model/tests/*.py \
	src/*.py tests/*.py
	@src/utils/center.sh "Running Flake8"
	flake8 --exit-zero \
	src/t_junction_model/*.py \
	src/utils/*.py \
	src/t_junction_model/tests/*.py \
	src/*.py \
	tests/*.py
	@echo ""
	@src/utils/center.sh "Running MyPy"
	mypy src/t_junction_model/*.py \
	src/utils/*.py \
	src/t_junction_model/tests/*.py \
	src/*.py \
	tests/*.py
	@echo ""
	@src/utils/center.sh "Done, see above for test results!"

# Generate badges for README showing:
# - number of tests
# - test coverage
# - Flake8 status
badges:
	@src/utils/center.sh "Generating Tests Badge"
	coverage run -m pytest -v \
	--junitxml=./.reports/tests/tests.xml \
	src/t_junction_model/*.py \
	src/utils/*.py \
	src/t_junction_model/tests/ \
	src/*.py \
	tests/
	genbadge tests \
	-i ./.reports/tests/tests.xml \
	-o ./.reports/tests/tests_badge.svg
	@src/utils/center.sh "Generating Test Coverage Badge"
	coverage xml \
	--skip-empty \
	-o ./.reports/coverage/coverage_all.xml
	genbadge coverage \
	-n "total coverage" \
	-i ./.reports/coverage/coverage_all.xml \
	-o ./.reports/coverage/coverage_all_badge.svg
	coverage xml \
	--skip-empty \
	--omit src/make_figures.py,src/utils/formatter_class.py,tests/*.py \
	-o ./.reports/coverage/coverage_t_junction_models.xml
	genbadge coverage \
	-n "t_junction_model coverage" \
	-i ./.reports/coverage/coverage_t_junction_models.xml \
	-o ./.reports/coverage/coverage_t_junction_models_badge.svg
	@src/utils/center.sh "Generating Flake8 Badge"
	flake8 \
	src/t_junction_model/*.py \
	src/t_junction_model/tests/*.py \
	src/utils/*.py \
	src/*.py \
	tests/*.py \
	--exit-zero \
	--statistics \
	--tee --output-file \
	./.reports/flake8/flake8stats.txt
	genbadge flake8 \
	-i ./.reports/flake8/flake8stats.txt \
	-o ./.reports/flake8/flake8_badge.svg
	
