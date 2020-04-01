upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*
clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc build dist tests/reports docs/build .pytest_cache .tox .coverage
	rm -rf mpu.egg-info lambda.zip venv-lambda
	rm -rf __pycache__ mpu/datastructures/trie/__pycache__ mpu/__pycache__ mpu/units/__pycache__ tests/__pycache__
package:
	make clean
	./create_package.sh
muation-test:
	mutmut run
bandit:
	bandit -r mpu
