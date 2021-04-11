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

processed_messages = []


class MessageConsumer(Thread):
    def __init__(self, queue: Queue, acquire_timeout=3, timeout=10):
        super().__init__()
        self.done = False
        self.queue = queue
        self.queue_message = None
        self.result = False
        self.delete_on_finish = True
        self.acquire_timeout = acquire_timeout
        self.timeout = timeout

    def run(self):
        global processed_messages
        try:
            self.queue_message = self.queue.get(
                acquire_timeout=self.acquire_timeout, timeout=self.timeout
            )
            self.result = True
            while not self.done:
                time.sleep(0.1)
            if self.delete_on_finish:
                processed_messages.append(self.queue_message.id)
                self.queue.delete(self.queue_message.id)
        except:
            pass


class MessageFeeder(Thread):
    def __init__(self, queue: Queue, id: str, content: Any, timeout=10):
        super().__init__()
        self.done = False
        self.queue = queue
        self.id = id
        self.content = content
        self.result = False
        self.timeout = timeout

    def run(self):
        try:
            self.queue.put(self.id, self.content, timeout=self.timeout)
            self.result = True
        except:
            pass


class TestMulthreadQueue(unittest.TestCase):
    def setUp(self):
        global processed_messages
        processed_messages = []

    # @unittest.skip("Advanced Test 1")
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

    # @unittest.skip("Advanced Test 2")
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

    # @unittest.skip("Advanced Test 3")
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

    @unittest.skip("Advanced Test 4")
    def test_lock_usage(self):
        global processed_messages

        queue = Queue(maxsize=1)
        feeder_threads = []
        consumer_threads = []

        for i in range(25):
            feeder_threads.append(
                MessageFeeder(
                    queue, f"{i}.txt", {"content": "file content"}, timeout=60
                )
            )
            feeder_threads[-1].start()

        for i in range(25):
            consumer_threads.append(
                MessageConsumer(queue, acquire_timeout=10, timeout=90)
            )
            consumer_threads[-1].start()
            consumer_threads[-1].done = True

        for t in consumer_threads:
            t: MessageConsumer
            t.join()
            self.assertTrue(t.result)

        self.assertEqual(len(processed_messages), 25)
        for i in range(25):
            self.assertIn(f"{i}.txt", processed_messages)

        for t in feeder_threads:
            t: MessageFeeder
            t.join()
            self.assertTrue(t.result)

    def tearDown(self):
        pass
