from collections import OrderedDict
from threading import RLock, Condition
from typing import Any
import time


class Empty(Exception):
    def __init__(self) -> None:
        super().__init__("Queue is empty")


class Full(Exception):
    def __init__(self) -> None:
        super().__init__("Queue is full")


class RepeatedMessage(Exception):
    def __init__(self) -> None:
        super().__init__("The message is already registered on queue")


class DeleteAttemptToUnknownMessage(Exception):
    def __init__(self) -> None:
        super().__init__(
            "The message you tried to delete was already deleted or don't exists"
        )


class QueueMessage:
    def __init__(self, id: str, content: Any, timeout: int = None):
        self.id = id
        self.content = content
        self.timeout = timeout


class Queue:
    """This class implements multi-producer, multi-consumer FIFO queue.
    The main objective of Queue is to create a list of tasks for asynchronous processing
    """

    def __init__(self, maxsize) -> None:
        self._maxsize = maxsize
        self._queue = OrderedDict()
        self._lock = RLock()
        self._not_full = Condition(self._lock)
        self._not_empty = Condition(self._lock)

    def put(self, id: str, content: Any, timeout: int = 10):
        """Put an message into the queue.
        The 'id' and 'content' values are used to create a new QueueMessage and into the Queue.
        If the queue is full it will try to put the message for 'timeout' seconds before raise a Full Exception.
        """

        if timeout < 0:
            raise ValueError

        if id in self._queue:
            raise RepeatedMessage

        with self._not_full:
            if not self.full() or self._not_full.wait(timeout):
                queue_message = QueueMessage(id, content)
                self._queue[id] = queue_message
                self._not_empty.notify()
                return
        raise Full

    def qsize(self) -> int:
        """Return the size of the queue."""

        with self._lock:
            return len(self._queue)

    def full(self) -> bool:
        """Return True if the queue is full."""
        return 0 < self._maxsize <= self.qsize()

    def get(self, timeout: int = 10, acquire_timeout: int = 10) -> QueueMessage:
        """Return an message from the queue. This message is 'hidden' from the queue until its deletion or 'acquire_timeout' is reached.
        'timeout' arg inform how long the Queue object should try to get the message if the queue is empty before raising the `Empty` error.
        'acquire_timeout' arg value inform how long the thread wants to have this message for itself, if the message is not deleted it should be available in the queue after this time.
        """

        if timeout < 0 or acquire_timeout < 0:
            raise ValueError

        with self._not_empty:
            max_timeout = min_timeout = time.monotonic() + timeout
            while max_timeout > time.monotonic():
                if self.qsize() > 0:
                    for id in self._queue:
                        if (
                            self._queue[id].timeout is None
                            or self._queue[id].timeout < time.monotonic()
                        ):
                            self._queue[id].timeout = time.monotonic() + acquire_timeout
                            return self._queue[id]
                        else:
                            if self._queue[id].timeout < min_timeout:
                                min_timeout = self._queue[id].timeout
                self._not_empty.wait(min_timeout - time.monotonic())

        raise Empty

    def delete(self, id: str) -> None:
        """Removes the message from the queue"""

        with self._lock:
            if id in self._queue:
                del self._queue[id]
                self._not_full.notify()
                return

            raise DeleteAttemptToUnknownMessage
