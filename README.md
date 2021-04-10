# QueueTest

[![Build Status](https://img.shields.io/badge/Python-3.9.1-blue)](https://img.shields.io/badge/Python-3.9.1-blue)

As it's name suggest, QueueTest is a blockable queue of messages/tasks.
The main objective of QueueTest is to create a list of tasks for asyncronous processing.

The implementation must garantee:
- All messages/tasks on QueueTest **must be** processed. (If a thread couldn't process a message, it should go back to the queue)
- To provide a messages/tasks to a single thread on a multithread aplication. (Multhreads can't get the same message/task to avoid processing waste.)

Queue Behavior/Rules:
- A Queue is initially empty (without any messages)
- On instantiating a Queue, you must choose the max size of it (you can use `0` as infinite size).
- A Queue object must have a `qsize` method, which returns the number of messages inside it.
- A Queue object must have a `full` method, which returns if the queue is full or not.
- A Queue object must have a `put` method. This method must receive an `str` object as id, an "any type" object as content and an `integer` object as timeout.
    - huh


## How to Install? 🤘

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
## How to Test? ⚗️

Execute the following command to run tests.

```bash
python -m pytest
```

### Linter

QueueTest uses [black formatting linter](https://github.com/psf/black), the pytest will check the linter usage and will fail if your code isn't respecting it.