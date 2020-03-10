"""PyPI packages"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .base import (Attribute, DateTimeAttribute, DictAttribute, ListAttribute,
                   Serializable, SerializableMapping, SerializableSequence)

__all__ = [
    'PyPiPackage',
]


@dataclass
class PyPiPackageInfo(Serializable):
    """PyPI package information"""

    author = Attribute()
    author_email = Attribute()
    bugtrack_url = Attribute()
    classifiers = ListAttribute()
    description = Attribute()
    description_content = Attribute()
    docs_url = Attribute()
    download_url = Attribute()
    home_page = Attribute()
    license = Attribute()
    maintainer = Attribute()
    maintainer_email = Attribute()
    name = Attribute()
    package_url = Attribute()
    platform = Attribute()
    project_url = Attribute()
    release_url = Attribute()
    requires_dist = ListAttribute()
    requires_python = Attribute()
    summary = Attribute()
    version = Attribute()


@dataclass
class PyPiDigests(Serializable):
    """PyPI digests"""

    md5 = Attribute()
    sha256 = Attribute()


@dataclass
class PyPiUrl(Serializable):
    """PyPI URL"""

    comment_text = Attribute()
    digests = DictAttribute(type=PyPiDigests)
    filename = Attribute()
    has_sig = Attribute()
    packagetype = Attribute()
    python_version = Attribute()
    requires_python = Attribute()
    size = Attribute()
    upload_time = DateTimeAttribute()
    upload_time_iso_8601 = DateTimeAttribute()
    url = Attribute()


@dataclass
class PyPiUrls(SerializableSequence):
    """PyPI URLs"""

    type: Callable = PyPiUrl


@dataclass
class PyPiReleases(SerializableMapping):
    """PyPI releases"""

    type: Callable = PyPiUrls


@dataclass
class PyPiPackage(Serializable):
    """A PyPI package"""

    info = Attribute(type=PyPiPackageInfo)
    releases = DictAttribute(type=PyPiReleases)
    urls = ListAttribute(type=PyPiUrls)
