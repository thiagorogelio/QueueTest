import unittest
from src.queue import DeleteAttemptToUnknownMessage, Queue, Full, RepeatedMessage, Empty
import time


class TestQueue(unittest.TestCase):
    def setUp(self):
        pass

    def test_put(self):
        queue = Queue(maxsize=1)

        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        with self.assertRaises(Full):
            queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=1)

        with self.assertRaises(Full):
            queue.put("1.txt", {"abc": "whatever"}, block=False)

        with self.assertRaises(ValueError):
            queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=-4)

        queue = Queue(maxsize=2)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

        with self.assertRaises(RepeatedMessage):
            queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=1)

        queue = Queue(maxsize=0)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"abc": "whatever"}, block=False)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

    def test_get(self):
        queue = Queue(maxsize=1)

        with self.assertRaises(Empty):
            queue.get(block=True, timeout=1)

        with self.assertRaises(Empty):
            queue.get(block=False)

        with self.assertRaises(ValueError):
            queue.get(block=True, timeout=-4)

        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        queue_message = queue.get(block=True, timeout=1)
        self.assertEqual(queue_message.value, {"abc": "whatever"})

        queue = Queue(maxsize=1)

        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        queue_message = queue.get(block=False)
        self.assertEqual(queue_message.value, {"abc": "whatever"})

    def test_delete(self):
        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue_message = queue.get(block=True, timeout=1, acquire_timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.value, {"abc": "whatever"})
        self.assertEqual(queue_message.id, "1.txt")

        queue.delete(queue_message.id)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        with self.assertRaises(Empty):
            queue.delete(queue_message.id)

        with self.assertRaises(Empty):
            queue.delete(queue_message.id, block=False)

        with self.assertRaises(ValueError):
            queue.delete(queue_message.id, timeout=-30)

        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        queue_message = queue.get(block=True, timeout=1, acquire_timeout=10)

        with self.assertRaises(DeleteAttemptToUnknownMessage):
            queue.delete("obiwan")

        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue.delete(queue_message.id, block=False)

        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

    def test_acquire_timeout(self):
        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        queue.put("1.txt", {"abc": "whatever"}, block=True, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue_message = queue.get(block=True, timeout=1, acquire_timeout=0.1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.value, {"abc": "whatever"})
        self.assertEqual(queue_message.id, "1.txt")

        time.sleep(0.5)

        queue_message = queue.get(block=True, timeout=1, acquire_timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.value, {"abc": "whatever"})
        self.assertEqual(queue_message.id, "1.txt")

        with self.assertRaises(Empty):
            queue_message = queue.get(block=True, timeout=1, acquire_timeout=10)

    def tearDown(self):
        pass
