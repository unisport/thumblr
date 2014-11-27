import os
from setuptools import setup
from pip.req import parse_requirements

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_reqs = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements/requirements.txt'))
reqs = [str(install_requerement.req) for install_requerement in install_reqs]

setup(
    name='thumblr',
    version='0.1',
    packages=['thumblr'],
    include_package_data=True,
    description='Thumblr is an app that provides an abstraction to deal with '
                'images throughout the storefront project.',
    long_description=README,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=reqs
)