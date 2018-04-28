# core modules
from setuptools import find_packages
from setuptools import setup

config = {
    'name': 'mpu',
    'version': '0.1.0',
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'scripts': [],
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/mpu',
    'license': 'MIT',
    'description': 'Martins Python Utilities',
    'long_description': ('In case the batteries are not enough anymore.'),
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
                    'Topic :: Scientific/Engineering :: Information Analysis',
                    'Topic :: Software Development',
                    'Topic :: Utilities'],
    'zip_safe': True,
}

setup(**config)
