import unittest
import time
from threading import Thread
from typing import Any

from src.queue import (
    DeleteAttemptToUnknownMessage,
    Queue,
    Full,
    RepeatedMessage,
    Empty,
    QueueMessage,
)


class MessageConsumer(Thread):
    def __init__(self, queue: Queue):
        super().__init__()
        self.done = False
        self.queue = queue
        self.queue_message = None
        self.result = False
        self.delete_on_finish = True

    def run(self):
        try:
            self.queue_message = self.queue.get(acquire_timeout=3, timeout=10)
            self.result = True
            while not self.done:
                time.sleep(0.1)
            if self.delete_on_finish:
                self.queue.delete(self.queue_message.id)
        except:
            pass


class MessageFeeder(Thread):
    def __init__(self, queue: Queue, id: str, content: Any):
        super().__init__()
        self.done = False
        self.queue = queue
        self.id = id
        self.content = content
        self.result = False

    def run(self):
        try:
            self.queue.put(self.id, self.content, timeout=10)
            self.result = True
        except:
            pass


class TestMulthreadQueue(unittest.TestCase):
    def setUp(self):
        pass

    # @unittest.skip("Advanced Test")
    def test_timeout_put(self):
        queue = Queue(maxsize=1)
        t1 = MessageFeeder(queue, "1.txt", {"content": "file content"})
        t1.start()
        t1.join()
        self.assertTrue(t1.result)
        t2 = MessageFeeder(queue, "2.txt", {"content": "file content"})
        t2.start()

        time.sleep(1)
        t3 = MessageConsumer(queue)
        t3.start()
        t3.done = True
        t3.join()
        self.assertTrue(t3.result)

        t2.join()
        self.assertTrue(t2.result)

    def test_timeout_get(self):

        queue = Queue(maxsize=1)
        t1 = MessageConsumer(queue)
        t1.start()

        time.sleep(1)
        t2 = MessageFeeder(queue, "1.txt", {"content": "file content"})
        t2.start()
        t2.join()
        self.assertTrue(t2.result)

        t1.done = True
        t1.join()
        self.assertTrue(t1.result)

        self.assertEqual(queue.qsize(), 0)

    def test_timeout_get_by_acquire_timeout(self):

        queue = Queue(maxsize=1)
        t1 = MessageFeeder(queue, "1.txt", {"content": "file content"})
        t1.start()
        t1.join()
        self.assertTrue(t1.result)
        self.assertEqual(queue.qsize(), 1)

        t2 = MessageConsumer(queue)
        t2.start()
        t2.delete_on_finish = False
        t2.done = True

        t3 = MessageConsumer(queue)
        t3.start()
        t3.done = True

        t2.join()
        t3.join()

        self.assertTrue(t2.result)
        self.assertTrue(t3.result)
        self.assertEqual(queue.qsize(), 0)

    def tearDown(self):
        pass
