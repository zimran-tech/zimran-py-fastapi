from os import environ

from setuptools import find_namespace_packages, setup

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

with open('requirements/base.txt', encoding='utf-8') as file:
    install_requires = file.read().splitlines()

setup(
    name='zimran-fastapi',
    version=environ['GITHUB_REF_NAME'],
    description='Preconfigured FastAPI application',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=['zimran.*']),
    install_requires=install_requires,
    python_requires='>=3.11',
    zip_file=False,
)
