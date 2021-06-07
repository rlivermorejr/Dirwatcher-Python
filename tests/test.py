import sys
import unittest
import importlib
import subprocess

__author__ = """Russell Livermore"""

PKG_NAME = 'dirwatcher'


class test_dirwatcher(unittest.TestCase):
    """Only tests the author string and flake8"""

    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        cls.assertGreaterEqual(cls, sys.version_info[0], 3)
        cls.module = importlib.import_module(PKG_NAME)

    def test_flake8(self):
        """Checking PEP8/flake8"""
        result = subprocess.run(['flake8', self.module.__file__])
        self.assertEqual(result.returncode, 0)

    def test_author(self):
        """Checking author string"""
        self.assertNotEqual(self.module.__author__, '???')

    """I gave up on writing test because I don't have time,
    I barely have time to get the actual assignment done."""


if __name__ == '__main__':
    unittest.main(verbosity=2)
