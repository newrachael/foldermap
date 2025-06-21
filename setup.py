from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Read version from __init__.py
with open(os.path.join('foldermap', '__init__.py'), encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split("'")[1]
            break

setup(
    name="foldermap",
    version=version,
    author="Raykim",
    author_email="enro2414@gmail.com",
    description="A tool for mapping files and folders to markdown documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/newrachael/foldermap",
    packages=find_packages(),
    install_requires=[
        "pathspec>=0.9.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "foldermap=foldermap.cli:main",
        ],
    },
)