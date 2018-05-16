# core modules
from setuptools import find_packages
from setuptools import setup

# internal modules
exec(open('mpu/_version.py').read())

config = {
    'name': 'mpu',
    'version': __version__,
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'package_data': {'mpu': ['units/currencies.csv']},
    'scripts': [],
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/mpu',
    'license': 'MIT',
    'description': 'Martins Python Utilities',
    'long_description': ('In case the batteries are not enough anymore.\n'
                         'Have a look at https://github.com/MartinThoma/mpu '
                         'for documentation.'),
    'install_requires': [],
    'keywords': ['utility'],
    'download_url': 'https://github.com/MartinThoma/mpu',
    'classifiers': ['Development Status :: 1 - Planning',
                    'Environment :: Console',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Natural Language :: English',
                    'Programming Language :: Python :: 3.5',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': True,
}

setup(**config)
