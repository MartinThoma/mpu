maint:
	pip install -r requirements/dev.txt
	pre-commit autoupdate && pre-commit run --all-files
	pip-compile -U docs/requirements.in
	pip-compile -U setup.py -o requirements/prod.txt
	pip-compile -U requirements/ci.in
	pip-compile -U requirements/dev.in

upload:
	make clean
	python setup.py sdist bdist_wheel && twine upload dist/*

clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc build dist tests/reports docs/build .pytest_cache .tox .coverage html/
	rm -rf mpu.egg-info lambda.zip venv-lambda
	rm -rf __pycache__ mpu/datastructures/trie/__pycache__ mpu/__pycache__ mpu/units/__pycache__ tests/__pycache__

package:
	make clean
	./create_package.sh

mutation-test:
	mutmut run

mutmut-results:
	mutmut junitxml --suspicious-policy=ignore --untested-policy=ignore > mutmut-results.xml
	junit2html mutmut-results.xml mutmut-results.html

bandit:
	# Python3 only: B322 is save
	bandit -r mpu -s B322
