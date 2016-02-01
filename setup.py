try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import sys

config = {
    'description': 'systool is a library for system manipulation',
    'author': 'Matthew Conley',
    'url': 'https://github.com/mtconley/systools',
    'download_url': 'https://github.com/mtconley/systools.git.',
    'author_email': '',
    'version': '0.0.1',
    'install_requires': ['pyprind'],
    'packages': find_packages(),
    'name': 'systools'
}

print "system is: " + sys.platform
print ''
print "installing dependencies... "
print config['install_requires']

setup(**config)
