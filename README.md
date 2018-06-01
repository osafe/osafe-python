# OSafe Python

A Python implementation of OSafe.

## Requirements

-  Python 3.6+

## Installation

```bash
# use --user unless in virtual env
pip3.6 install osafe --user
```

## Usage

```bash
osafe
```

That's it!

## Distribute

```bash
python3.6 -m venv venv
. venv/bin/activate

pip install --upgrade pip setuptools wheel twine
rm -rf dist/
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
