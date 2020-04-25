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
    install_requires=[
        "aniso8601==8.0.0",
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "click==7.1.1",
        "dataclasses-json==0.4.2",
        "flask==1.1.2",
        "flask-cors==3.0.8",
        "flask-restful==0.3.8",
        "flask-wtf==0.14.3",
        "h11==0.9.0",
        "h2==3.2.0",
        "hpack==3.0.0",
        "hstspreload==2020.4.24",
        "httpx==0.12.1",
        "hyperframe==5.2.0",
        "idna==2.9",
        "itsdangerous==1.1.0",
        "jinja2==2.11.2",
        "markupsafe==1.1.1",
        "marshmallow==3.5.1",
        "marshmallow-enum==1.5.1",
        "mypy-extensions==0.4.3",
        "orjson==2.6.6",
        "psycopg2-binary==2.8.5",
        "punq==0.4.1",
        "pytz==2019.3",
        "returns==0.13.0",
        "rfc3986==1.4.0",
        "six==1.14.0",
        "sniffio==1.1.0",
        "sqlalchemy==1.3.16",
        "stringcase==1.2.0",
        "typing-extensions==3.7.4.2",
        "typing-inspect==0.5.0",
        "urllib3==1.25.9",
        "werkzeug==1.0.1",
        "wtforms==2.3.1",
    ],
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