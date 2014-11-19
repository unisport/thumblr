import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='thumblr',
    version='0.1',
    packages=['thumblr'],
    include_package_data=True,
    description='Thumblr is an app that provides an abstraction to deal with '
                'images throughout the storefront project.',
    long_description=README,
    url='http://www.example.com/',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=['django>=1.6.0',
                      'south>=0.8',
                      'boto>=2.0.',
                      'jsonfield>=1',
                      'Pillow>=2',
                      'celery>3',
                      ],
)