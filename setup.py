#!/usr/bin/env python

import re

import setuptools

with open('gorinich/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setuptools.setup(
    name='gorinich',
    version=version,
    description='Gorinich Collaboration System',
    author='Taras Drapalyuk',
    author_email='taras@drapalyuk.com',
    license='BSD',
    url="http://gorinich.drapalyuk.com/",
    packages=setuptools.find_packages(exclude=('tests', 'tests.*')),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'sockjs-tornado==1.0.1',
        'Jinja2>=2.7.3,<3.0.0'
    ],
)
