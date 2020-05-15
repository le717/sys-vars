# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


# Get the package's longer description
# (usually located in the README file)
with open("./README.md", "rt", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="docker_secrets",
    version="2.0.0",
    description="Small Python module for easily accessing Docker secrets.",
    url="https://github.com/le717/python-docker-secrets",
    license="The MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Caleb Ely",
    author_email="le717@users.noreply.github.com",
    python_requires=">=3.5",
    package_dir={"": "docker_secrets"},
    py_modules=find_packages()
)
