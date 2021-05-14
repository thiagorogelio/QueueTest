# QueueTest

[![Build Status](https://img.shields.io/badge/Python-3.9.1-blue)](https://img.shields.io/badge/Python-3.9.1-blue)

As its name suggests, QueueTest is a queue of messages/tasks.

## Part 1.

(In this part you don't need to worry about multithreading)

Implement the Queue class given the following Behavior/Rules:
- A Queue is initially empty (without any messages)
- On instantiating a Queue, you must choose the max size of it (you can use `0` as infinite size).
- A Queue object must have a `put` method, which inserts a message into the Queue. This method must receive an `str` object as **id**, an "any type" object as **content**.
    - The **id** and **content** values must be used to create a new QueueMessage object and then, saved into the Queue.
    - This method must raise a `Full` error if the queue is full.
    - If an already existing **id** is informed, the method should raise the `RepeatedMessage` error.
- A Queue object must have a `qsize` method, which returns the number of messages inside it.
- A Queue object must have a `full` method, which returns if the queue is full or not.
- A Queue object must have a `get` method, which returns a QueueMessage object.
    - This method must raise an `Empty` error if the queue is empty.
- A Queue object must have a `delete` method, which removes the message from the queue. This method must receive an `str` object as id.
    - A Queue object must raise a `DeleteAttemptToUnknownMessage` error if the Id doesn't exist on the queue.
- These are the only public methods that must exist. You can create any number of private methods that you want, as long as you use the prefix `_` to them.

## Part 2.

The main objective of QueueTest is to create a list of tasks for asynchronous multi-producer, multi-consumer processing.
- Now you have to worry about multithreading. 
- The implementation must guarantee that all messages/tasks on QueueTest **must be** processed. (If a thread couldn't process a message, it should go back to the queue)
- A message/task is provided to a single thread on a multithread application. (multiple threads can't get the same message/task at the same time, to avoid processing waste.)

Alter the Queue class given the following Behavior/Rules:
- The `put` method must now have an optional parameter **timeout** with a default value of 10s.
    - If positive, the **timeout** value must be used to inform how long the Queue object should try to put the message while the queue is full before raising the `Full` error.
    - If an invalid number is sent in the **timeout** parameter, it should raise a `ValueError` error.
    - For better implementation, check if you should raise `ValueError`, and after that, you can check if you should raise `RepeatedMessage` error. For the last, check if you should raise `Full` error.
- The `get` method must now have:
    - A optional parameter **timeout** with a default value of 10s that inform how long the Queue object should try to get the message if the queue is empty before raising the `Empty` error.
    - A optional parameter **acquire_timeout** with a default value of 10s that inform how long the thread wants to have this object for itself. If another thread tries to get this message after this time, it should be available and not before.
    - If an invalid number is sent in the **timeout** or **acquire_timeout** parameter, it should raise a `ValueError` error.
    - For better implementation, check if you should raise `ValueError`. After that, you can check if you should raise `Empty` error.