from setuptools import setup, find_packages
from setuptools.command.install import install
from codecs import open
from os import path
from unittest import TestLoader

here = path.abspath(path.dirname(__file__))

class PostInstallMessage(install):
    def run(self):
        print "DEPRECATION WARNING: The swiftype_enterprise package has been deprecated and replaced by elastic_enterprise_search"
        install.run(self)

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

fh = open('README.md')
try:
    try:
        readme_content = fh.read()
    except:
        readme_content = ""
finally:
    f.close()

here = path.abspath(path.dirname(__file__))
about = {}
with open(path.join(here, 'swiftype_enterprise', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
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
    test_suite='tests',
    cmdclass={
        'install': PostInstallMessage,
    }
)
