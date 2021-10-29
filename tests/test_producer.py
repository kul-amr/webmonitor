import unittest
import logging
from src import *

logger = logging.getLogger(__name__)


class ProducerTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_without_regexp(self):
        test_web = "https://medium.com/"
        key, val = get_web_stats(test_web)
        self.assertEqual(key["website"], test_web)
        self.assertEqual(val["status_code"], 200)
        self.assertIsNotNone(val["response_time"])
        self.assertIsNone(val["regexp"])
        self.assertEqual(val["regexp_exists"], False)
        self.assertIsNotNone(val["create_datetime"])

    def test_with_regexp(self):
        test_web = "https://medium.com/"
        key, val = get_web_stats(test_web,regexp='TOPICS')
        self.assertEqual(key["website"], test_web)
        self.assertEqual(val["status_code"], 200)
        self.assertIsNotNone(val["response_time"])
        self.assertEqual(val["regexp"],'TOPICS')
        self.assertEqual(val["regexp_exists"], True)
        self.assertIsNotNone(val["create_datetime"])

    def test_with_incorrect_regexp(self):
        test_web = "https://medium.com/"
        key, val = get_web_stats(test_web, regexp='IncorrectTopic')
        self.assertEqual(key["website"], test_web)
        self.assertEqual(val["status_code"], 200)
        self.assertIsNotNone(val["response_time"])
        self.assertEqual(val["regexp"], 'IncorrectTopic')
        self.assertEqual(val["regexp_exists"], False)
        self.assertIsNotNone(val["create_datetime"])

    def test_with_incorrect_web(self):
        test_web = "https://mediumwrong.com/"
        key, val = get_web_stats(test_web)
        self.assertEqual(key["website"], test_web)
        self.assertEqual(val["status_code"], 0)
        self.assertIsNotNone(val["response_time"])
        self.assertIsNone(val["regexp"])
        self.assertEqual(val["regexp_exists"], False)
        self.assertIsNotNone(val["create_datetime"])


if __name__ == '__main__':
    unittest.main()
