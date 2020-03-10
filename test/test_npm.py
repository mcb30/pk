"""NPM tests"""

import sys
import unittest
from datetime import date
from pathlib import Path

from pk.npm import NpmPackage


class NpmPackageTest(unittest.TestCase):
    """NPM package tests"""

    @classmethod
    def setUpClass(cls):
        cls.files = Path(sys.modules[cls.__module__].__file__).parent / 'files'

    def test_json(self):
        """Test JSON parsing"""
        npm = NpmPackage(json=(self.files / 'leftpad.json').read_text())
        self.assertEqual(npm.author.name, "Tom MacWright")
        self.assertEqual(npm.dist_tags.latest, '0.0.1')
        self.assertEqual(npm.dist_tags['latest'], '0.0.1')
        self.assertEqual(npm.time.modified.date(), date(2018, 2, 27))
        self.assertEqual(npm.time['0.0.1'].date(), date(2017, 5, 3))
        self.assertFalse(npm.users)
        self.assertEqual(npm.versions['0.0.0'].bugs.url,
                         'https://github.com/tmcw/leftpad/issues')
        self.assertIn('formatting', npm.versions['0.0.0'].keywords)
        self.assertEqual(npm.versions['0.0.1'].maintainers[0].name, 'tmcw')
        self.assertEqual(npm.versions['0.0.1'].repository.type, 'git')
        self.assertEqual(npm.versions['0.0.1'].devDependencies['jsverify'],
                         '^0.8.2')
        self.assertEqual(npm.versions['0.0.1'].dist.shasum,
                         '86b1a4de4face180ac545a83f1503523d8fed115')
