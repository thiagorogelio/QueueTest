from typing import Any
import time
from threading import Lock, Condition


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
    def __init__(self, id: str, content: Any):
        self.id = id
        self.content = content
        self._released_at = time.time()


class Queue(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.queue = {}
        self._not_empty = Lock()
        self._not_full = Lock()

    def get(self, timeout=10, acquire_timeout=10):

        if timeout < 0:
            raise ValueError()

        trying_since = time.time()
        acquired = False
        while time.time() - trying_since < timeout:
            acquired = self._not_empty.acquire(blocking=True, timeout=0.1)
            if acquired:
                if not self._empty():
                    break
                else:
                    self._not_empty.release()
                    time.sleep(0.1)

        if not acquired or self._empty():
            raise Empty()

        message = self._get_not_used_queue(acquire_timeout)

        while message is None and time.time() - trying_since < timeout:
            message = self._get_not_used_queue(acquire_timeout)

        self._not_empty.release()

        if message is None:
            raise Empty()

        return message

    def _get_not_used_queue(self, acquire_timeout):
        for message in self.queue.values():
            message: QueueMessage
            if time.time() > message._released_at:
                time.sleep(0.5)
                message._released_at = time.time() + acquire_timeout
                return message

        return None

    def put(self, id, content, timeout=10):

        if timeout < 0:
            raise ValueError()

        if id in self.queue:
            raise RepeatedMessage()

        trying_since = time.time()
        acquired = False
        while time.time() - trying_since < timeout:
            if not self.full():
                acquired = self._not_full.acquire(blocking=True, timeout=0.1)
                if acquired:
                    break
            else:
                time.sleep(0.1)

        if self.full():
            if acquired:
                self._not_full.release()
            raise Full()

        self.queue[id] = QueueMessage(id, content)
        if acquired:
            self._not_full.release()

    def delete(self, id):

        if id not in self.queue:
            raise DeleteAttemptToUnknownMessage()

        del self.queue[id]

    def qsize(self):
        message = len(self.queue.keys())
        return message

    def full(self):
        _full = False if self.maxsize == 0 else len(self.queue.keys()) == self.maxsize
        return _full

    def _empty(self):
        empty = len(self.queue.keys()) == 0
        return empty
