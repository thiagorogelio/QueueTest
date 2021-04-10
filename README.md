# QueueTest

[![Build Status](https://img.shields.io/badge/Python-3.9.1-blue)](https://img.shields.io/badge/Python-3.9.1-blue)

## Install 🤘

The following steps covers the setup process

### Using pyenv with pyenv-virtualenv

You should use virtualenv to build/develop the project and I recommend the use of [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to manage multiple python environments.

```bash
pyenv install 3.9.1
pyenv virtualenv 3.9.1 QueueTest
pyenv activate QueueTest
```
### Installing dependencies (Python 3.9.1)

Open your bash and run the follow command to install all the project dependencies, you just need to run the command one time

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
## Tests ⚗️

Execute the following command to run tests.

```bash
python -m pytest
```
