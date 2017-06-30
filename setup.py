from setuptools import setup, find_packages
from codecs import open
from os import path
from unittest import TestLoader

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

fh = open('README.rst')
try:
    try:
        readme_content = fh.read()
    except:
        readme_content = ""
finally:
    f.close()

setup(
    name='swiftype_enterprise',
    version='0.0.2',
    description='An API client for Swiftype Enterprise',
    long_description=readme_content,
    url='https://github.com/swiftype/swiftype-enterprise-python',
    author='Swiftype',
    author_email='eng@swiftype.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='swiftype enterprise search api',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'requests',
        'future'
    ],
    extras_require={
        'test': ['mock'],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'swiftype_enterprise=swiftype_enterprise:main',
        ],
    },
    test_suite='tests'
)
