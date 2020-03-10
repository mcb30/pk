"""PyPI tests"""

import sys
import unittest
from pathlib import Path

from pk.pypi import PyPiPackage


class PyPiPackageTest(unittest.TestCase):
    """PyPI package tests"""

    @classmethod
    def setUpClass(cls):
        cls.files = Path(sys.modules[cls.__module__].__file__).parent / 'files'

    def test_json(self):
        """Test JSON parsing"""
        pypi = PyPiPackage(json=(self.files / 'idiosync.json').read_text())
        self.assertEqual(pypi.info.author, "Michael Brown")
        self.assertEqual(pypi.info.summary, "Synchronize user databases")
        self.assertEqual(pypi.releases['0.0.1'][0].size, 22655)
        self.assertEqual(len(pypi.info.classifiers), 7)
        self.assertIn('Environment :: Console', pypi.info.classifiers)
        self.assertEqual(len(pypi.urls), 2)
        self.assertEqual(pypi.urls[1].filename, 'idiosync-0.0.1.tar.gz')
