# core modules
from setuptools import find_packages
from setuptools import setup
import os
import io

# internal modules
exec(open('mpu/_version.py').read())


def read(file_name):
    """Read a text file and return the content as a string."""
    with io.open(os.path.join(os.path.dirname(__file__), file_name),
                 encoding='utf-8') as f:
        return f.read()

config = {
    'name': 'mpu',
    'version': __version__,
    'author': 'Martin Thoma',
    'author_email': 'info@martin-thoma.de',
    'maintainer': 'Martin Thoma',
    'maintainer_email': 'info@martin-thoma.de',
    'packages': find_packages(),
    'package_data': {'mpu': ['units/currencies.csv']},
    'extras_require': {'all': ['pandas']},
    'scripts': [],
    'platforms': ['Linux'],
    'url': 'https://github.com/MartinThoma/mpu',
    'license': 'MIT',
    'description': 'Martins Python Utilities',
    'long_description': read('README.md'),
    'long_description_content_type': 'text/markdown',
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
