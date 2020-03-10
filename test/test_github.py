"""GitHub tests"""

import os
import sys
import unittest
from datetime import date
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from requests import Response, Session

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

    def test_token(self):
        """Test token authentication"""
        url = 'https://api.github.com/repos/mcb30/ipxe'
        rsp = Response()
        rsp.status_code = 200
        rsp.raw = BytesIO(b'{}')
        with patch.object(Session, 'send', return_value=rsp) as send:
            with patch.dict(os.environ, {'GITHUB_TOKEN': 'secret'}):
                GitHubRepo.fetch_json(url)
                send.assert_called_once()
                self.assertEqual(send.call_args[0][0].headers['Authorization'],
                                 'token secret')
                send.reset_mock()
                del os.environ['GITHUB_TOKEN']
                GitHubRepo.fetch_json(url)
                send.assert_called_once()
                self.assertNotIn('Authorization', send.call_args[0][0].headers)
