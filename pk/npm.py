"""NPM packages

The NPM package metadata format is documented at
https://github.com/npm/registry/blob/master/docs/responses/package-metadata.md
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .base import (Attribute, DateTimeAttribute, DictAttribute, ListAttribute,
                   Serializable, SerializableMapping, SerializableSequence)

__all__ = [
    'NpmPackage',
]


@dataclass
class NpmHuman(Serializable):
    """NPM human object"""

    name = Attribute()
    email = Attribute()
    url = Attribute()


@dataclass
class NpmHumans(SerializableSequence):
    """NPM human objects"""

    type: Callable = NpmHuman


@dataclass
class NpmDist(Serializable):
    """NPM dist object"""

    tarball = Attribute()
    shasum = Attribute()


@dataclass
class NpmRepository(Serializable):
    """NPM repository object"""

    type = Attribute()
    url = Attribute()


@dataclass
class NpmTime(SerializableMapping):
    """NPM publication times"""

    type: Callable = DateTimeAttribute.type

    created = DateTimeAttribute()
    modified = DateTimeAttribute()


@dataclass
class NpmDistTags(SerializableMapping):
    """NPM dist tags"""

    latest = Attribute()


@dataclass
class NpmVersionHoisted(Serializable):
    """NPM hoisted version information"""

    author = Attribute(type=NpmHuman)
    bugs = Attribute(type=NpmHuman)
    contributors = ListAttribute(type=NpmHumans)
    description = Attribute()
    homepage = Attribute()
    keywords = ListAttribute()
    license = Attribute()
    maintainers = ListAttribute(type=NpmHumans)
    readme = Attribute()
    readmeFilename = Attribute()
    repository = Attribute(type=NpmRepository)


@dataclass
class NpmVersion(NpmVersionHoisted):
    """NPM package version"""

    name = Attribute()
    version = Attribute()
    deprecated = Attribute()
    dependencies = DictAttribute()
    optionalDependencies = DictAttribute()
    devDependencies = DictAttribute()
    bundleDependencies = DictAttribute()
    peerDependencies = DictAttribute()
    bin = DictAttribute()
    directories = DictAttribute()
    dist = Attribute(type=NpmDist)
    engines = DictAttribute()
    hasShrinkwap = Attribute('_hasShrinkwrap')
    id = Attribute('_id')
    nodeVersion = Attribute('_nodeVersion')
    npmUser = Attribute('_npmUser', type=NpmHuman)
    main = Attribute()


@dataclass
class NpmVersions(SerializableMapping):
    """NPM package versions"""

    type: Callable = NpmVersion


@dataclass
class NpmPackage(NpmVersionHoisted):
    """An NPM package"""

    id = Attribute('_id')
    rev = Attribute('_rev')
    dist_tags = Attribute('dist-tags', type=NpmDistTags)
    name = Attribute()
    time = Attribute(type=NpmTime)
    users = DictAttribute()
    versions = DictAttribute(type=NpmVersions)
