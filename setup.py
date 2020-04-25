from pathlib import Path
from setuptools import setup, find_packages

project_folder = Path(__file__).parent

with open(project_folder.joinpath("README.md")) as _file:
    long_description = _file.read()

setup(
    name="kamui",
    version="0.0.1",
    author="Pablo Henrique Aguilar",
    description="Tool to make easy streams creation on KSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thepabloaguilar/kamui",
    license="Apache-2.0",
    packages=find_packages(),
    install_requires=[],
    project_urls={
        "Documentation": "https://github.com/thepabloaguilar/kamui",
        "Source Code": "https://github.com/thepabloaguilar/kamui",
    },
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.7",
)
