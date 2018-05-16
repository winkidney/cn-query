import os
from setuptools import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))

requires = (
    "requests",
)


setup(
    name='cn-query',
    version='0.0.1',
    packages=find_packages(here),
    license='MIT',
    author='winkidney@gmail.com',
    description='The functioning ',
    install_requires=requires,
)
