from setuptools import setup, find_packages
from codecs import open
from os import path

base_dir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(base_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

about = {}
with open(
    path.join(base_dir, "elastic_workplace_search/__version__.py"), encoding="utf-8"
) as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    maintainer=about["__maintainer__"],
    maintainer_email=about["__maintainer_email__"],
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="elastic workplace search api",
    packages=find_packages(exclude=["tests"]),
    install_requires=["requests"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
)
