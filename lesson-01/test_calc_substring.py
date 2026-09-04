from unittest import TestCase

from calc_substring import is_substring


class TestIsSubstring(TestCase):

    def setUp(self):
        print("setUp")

    def test_empty(self):
        self.assertTrue(is_substring("", ""))
        self.assertTrue(is_substring("", "F"))
        self.assertTrue(is_substring("", "9"))
        self.assertTrue(is_substring("", "qwerty"))
        self.assertFalse(is_substring("qwerty", ""))
        self.assertFalse(is_substring("F", ""))
        self.assertFalse(is_substring("9", ""))

    def test_valid(self):
        self.assertTrue(is_substring("f", "f"))
        self.assertTrue(is_substring("asd", "asd"))
        self.assertTrue(is_substring("asd", "asdqwe"))
        self.assertTrue(is_substring("asd", "123asdqwe"))
        self.assertTrue(is_substring("asd", "123asd"))

        self.assertFalse(is_substring("asd1", "123asdqwe"))
        self.assertFalse(is_substring("3sd", "123asd"))

    def test_repite(self):
        self.assertTrue(is_substring("f", "fff"))
        self.assertTrue(is_substring("asd", "asdasd"))
        self.assertFalse(is_substring("fff", "ff"))
        self.assertTrue(is_substring("fff", "ffff"))
        self.assertTrue(is_substring("F", "fff"))


