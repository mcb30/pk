"""GitHub repositories

The GitHub repository metadata format is documented at
https://developer.github.com/v3/repos/
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from requests import PreparedRequest
from requests.auth import AuthBase

from .base import (Attribute, Base64Attribute, DateTimeAttribute,
                   ListAttribute, Serializable)

__all__ = [
    'GitHubRepo',
]


@dataclass
class GitHubUser(Serializable):
    """A GitHub user"""

    login = Attribute()
    id = Attribute()
    node_id = Base64Attribute()
    avatar_url = Attribute()
    gravatar_id = Attribute()
    url = Attribute()
    html_url = Attribute()
    followers_url = Attribute()
    following_url = Attribute()
    gists_url = Attribute()
    starred_url = Attribute()
    subscriptions_url = Attribute()
    organizations_url = Attribute()
    repos_url = Attribute()
    events_url = Attribute()
    received_events_url = Attribute()
    type = Attribute()
    site_admin = Attribute()


@dataclass
class GitHubPermissions(Serializable):
    """GitHub permissions"""

    admin = Attribute()
    push = Attribute()
    pull = Attribute()


@dataclass
class GitHubLicense(Serializable):
    """GitHub license"""

    key = Attribute()
    name = Attribute()
    spdx_id = Attribute()
    url = Attribute()
    node_id = Base64Attribute()


@dataclass
class GitHubRepo(Serializable):
    """A GitHub repository"""

    id = Attribute()
    node_id = Base64Attribute()
    name = Attribute()
    full_name = Attribute()
    owner = Attribute(type=GitHubUser)
    private = Attribute()
    html_url = Attribute()
    description = Attribute()
    fork = Attribute()
    url = Attribute()
    archive_url = Attribute()
    assignees_url = Attribute()
    blobs_url = Attribute()
    branches_url = Attribute()
    collaborators_url = Attribute()
    comments_url = Attribute()
    commits_url = Attribute()
    compare_url = Attribute()
    contents_url = Attribute()
    contributors_url = Attribute()
    deployments_url = Attribute()
    downloads_url = Attribute()
    events_url = Attribute()
    forks_url = Attribute()
    git_commits_url = Attribute()
    git_refs_url = Attribute()
    git_tags_url = Attribute()
    git_url = Attribute()
    issue_comment_url = Attribute()
    issue_events_url = Attribute()
    issues_url = Attribute()
    keys_url = Attribute()
    labels_url = Attribute()
    languages_url = Attribute()
    merges_url = Attribute()
    milestones_url = Attribute()
    notifications_url = Attribute()
    pulls_url = Attribute()
    releases_url = Attribute()
    ssh_url = Attribute()
    stargazers_url = Attribute()
    statuses_url = Attribute()
    subscribers_url = Attribute()
    subscription_url = Attribute()
    tags_url = Attribute()
    teams_url = Attribute()
    trees_url = Attribute()
    clone_url = Attribute()
    mirror_url = Attribute()
    hooks_url = Attribute()
    svn_url = Attribute()
    homepage = Attribute()
    language = Attribute()
    forks_count = Attribute()
    stargazers_count = Attribute()
    watchers_count = Attribute()
    size = Attribute()
    default_branch = Attribute()
    open_issues_count = Attribute()
    is_template = Attribute()
    topics = ListAttribute()
    has_issues = Attribute()
    has_projects = Attribute()
    has_wiki = Attribute()
    has_pages = Attribute()
    has_downloads = Attribute()
    archived = Attribute()
    disabled = Attribute()
    visibility = Attribute()
    pushed_at = DateTimeAttribute()
    created_at = DateTimeAttribute()
    updated_at = DateTimeAttribute()
    permissions = Attribute(type=GitHubPermissions)
    allow_rebase_merge = Attribute()
    template_repository = Attribute()
    temp_clone_token = Attribute()
    allow_squash_merge = Attribute()
    allow_merge_commit = Attribute()
    subscribers_count = Attribute()
    network_count = Attribute()
    license = Attribute(type=GitHubLicense)
    organization = Attribute(type=GitHubUser)
    parent = Attribute()
    source = Attribute()


GitHubRepo.parent.type = GitHubRepo
GitHubRepo.source.type = GitHubRepo


@dataclass
class GitHubTokenAuth(AuthBase):
    """GitHub API authentication via personal access token"""

    env: str = 'GITHUB_TOKEN'

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        token = os.environ.get(self.env)
        if token is not None:
            r.headers['Authorization'] = 'token %s' % token
        return r


GitHubRepo.register_auth('api.github.com', GitHubTokenAuth())
