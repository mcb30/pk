"""GitHub tests"""

from datetime import date
from pathlib import Path
import sys
import unittest
from pk.github import GitHubRepo


class GitHubRepoTest(unittest.TestCase):
    """GitHub repository tests"""

    @classmethod
    def setUpClass(cls):
        cls.files = Path(sys.modules[cls.__module__].__file__).parent / 'files'

    def test_json(self):
        """Test JSON parsing"""
        gh = GitHubRepo(json=(self.files / 'ipxe.json').read_text())
        self.assertEqual(gh.node_id, b'010:Repository85846560')
        self.assertEqual(gh.owner.login, 'mcb30')
        self.assertEqual(gh.owner.type, 'User')
        self.assertFalse(gh.owner.site_admin)
        self.assertTrue(gh.fork)
        self.assertEqual(gh.pushed_at.date(), date(2019, 12, 23))
        self.assertTrue(gh.permissions.push)
        self.assertEqual(gh.license.name, 'Other')
        self.assertEqual(gh.parent.owner.login, 'ipxe')
        self.assertEqual(gh.parent.html_url, 'https://github.com/ipxe/ipxe')
        self.assertEqual(gh.source.full_name, 'ipxe/ipxe')
        self.assertEqual(gh.source.forks_count, 254)
