"""
Simple client server unit test
"""

import logging
import threading
import unittest

import clientserver
from context import lab_logging

lab_logging.setup(stream_level=logging.INFO)


class TestEchoService(unittest.TestCase):
    """The test"""

    _database = {
        'annette':1234,
        'jack': 4098,
        'peter': 5678,
        'sape': 4139
    }
    _server = clientserver.Server()  # create single server in class variable
    _server_thread = threading.Thread(target=_server.start_phone_book)  # define thread for running server

    @classmethod
    def setUpClass(cls):
        cls._server_thread.start()  # start server loop in a thread (called only once)

    def setUp(self):
        super().setUp()
        self.client = clientserver.Client()  # create new client for each test

    def test_phone_get(self):  # each test_* function is a test
        """Test get"""
        msg = self.client.get("annette")
        self.assertEqual(msg, 'annette: 1234')

    def test_phone_get_all(self):
        """Test get_all"""
        msg = self.client.get_all()
        self.assertEqual(msg, 'annette: 1234\njack: 4098\npeter: 5678\nsape: 4139\n')

    def tearDown(self):
        self.client.close()  # terminate client after each test

    @classmethod
    def tearDownClass(cls):
        cls._server._serving = False  # break out of server loop. pylint: disable=protected-access
        cls._server_thread.join()  # wait for server thread to terminate


if __name__ == '__main__':
    unittest.main()
