upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*
clean:
	python setup.py clean --all
	pyclean .
	rm -rf *.pyc __pycache__ build dist mpu.egg-info mpu/__pycache__ mpu/units/__pycache__ lambda.zip venv-lambda tests/__pycache__ tests/reports docs/build .pytest_cache .tox .coverage
package:
	make clean
	./create_package.sh
muation-test:
	cosmic-ray init cr-config.toml cr_session.sqlite && cosmic-ray exec cr_session.sqlite && cr-html cr_session.sqlite > cr-report.html
