upload:
	make clean
	python3 setup.py sdist bdist_wheel && twine upload dist/*
clean:
	rm -rf *.pyc __pycache__ build dist mpu.egg-info mpu/__pycache__
package:
	make clean
	./create_package.sh
