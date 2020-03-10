"""Base classes"""

from __future__ import annotations

from base64 import b64decode
from collections.abc import Mapping, Sequence
from dataclasses import InitVar, dataclass, field
from datetime import datetime
from json import JSONDecoder, JSONEncoder
from typing import (Any, Callable, ClassVar, Iterator, MutableMapping,
                    Optional, Type, TypeVar, cast)
from urllib.parse import urlparse

import dateutil.parser

from requests import PreparedRequest, Session
from requests.auth import AuthBase

from yaml import safe_dump, safe_load

__all__ = [
    'Attribute',
    'DateTimeAttribute',
    'DictAttribute',
    'ListAttribute',
    'Serializable',
    'SerializableMapping',
    'SerializableSequence',
]


@dataclass
class PerHostAuth(AuthBase):
    """Per-host HTTPS authentication mechanisms"""

    hosts: MutableMapping[str, AuthBase] = field(default_factory=dict)

    def register(self, host: str, auth: AuthBase) -> None:
        """Register per-host HTTPS authentication mechanism"""
        self.hosts[host] = auth

    def __call__(self, r: PreparedRequest) -> PreparedRequest:
        if r.url is None:
            return r
        url = urlparse(r.url)
        if url.scheme != 'https':
            return r
        if url.hostname is None or url.hostname not in self.hosts:
            return r
        return self.hosts[url.hostname](r)


@dataclass
class Serializable:
    """Data structure serializable as JSON or YAML"""

    Self = TypeVar('Self', bound='Serializable')

    data: Any = None
    """Data structure"""

    json: InitVar[Optional[str]] = None
    yaml: InitVar[Optional[str]] = None

    _json_encoder: ClassVar[JSONEncoder] = JSONEncoder()
    _json_decoder: ClassVar[JSONDecoder] = JSONDecoder()
    _session: ClassVar[Session] = Session()

    def __post_init__(self, json: Optional[str], yaml: Optional[str]) -> None:
        json_default = type(self).json  # type: ignore[has-type]
        yaml_default = type(self).yaml  # type: ignore[has-type]
        if json is not None and json is not json_default:
            self.json = json
        if yaml is not None and yaml is not yaml_default:
            self.yaml = yaml

    def __str__(self) -> str:
        return self.yaml

    @property  # type: ignore[no-redef]
    def json(self) -> str:  # pylint: disable=function-redefined
        """JSON serialization"""
        return self._json_encoder.encode(self.data)

    @json.setter
    def json(self, value: str) -> None:
        self.data = self._json_decoder.decode(value)

    @classmethod
    def fetch_json(cls: Type[Self], uri: str) -> Self:
        """Fetch JSON from URI"""
        rsp = cls._session.get(uri)
        rsp.raise_for_status()
        if rsp.encoding is None:
            rsp.encoding = 'utf-8'
        return cls(json=rsp.text)

    @property  # type: ignore[no-redef]
    def yaml(self) -> str:  # pylint: disable=function-redefined
        """YAML serialization"""
        return safe_dump(self.data, sort_keys=False)

    @yaml.setter
    def yaml(self, value: str) -> None:
        self.data = safe_load(value)

    @classmethod
    def fetch_yaml(cls: Type[Self], uri: str) -> Self:
        """Fetch YAML from URI"""
        rsp = cls._session.get(uri)
        rsp.raise_for_status()
        return cls(yaml=rsp.text)

    @classmethod
    def register_auth(cls, host: str, auth: AuthBase) -> None:
        """Register per-host HTTPS authentication mechanism"""
        if cls._session.auth is None:
            cls._session.auth = PerHostAuth()
        assert isinstance(cls._session.auth, PerHostAuth)
        cls._session.auth.register(host, auth)


@dataclass
class SerializableSequence(Serializable, Sequence):
    """Data structure accessible as a sequence"""

    type: Callable = lambda x: x
    """Value type"""

    def __getitem__(self, key: Any) -> Any:
        return self.type(self.data[key])

    def __len__(self) -> int:
        return len(self.data)


@dataclass
class SerializableMapping(Serializable, Mapping):
    """Data structure accessible as a mapping"""

    type: Callable = lambda x: x
    """Value type"""

    def __getitem__(self, key: Any) -> Any:
        return self.type(self.data[key])

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)


@dataclass
class Attribute:
    """A data structure attribute"""

    name: str = cast(str, None)
    """Attribute name"""

    type: Callable = lambda x: x
    """Attribute type"""

    def __set_name__(self, owner: Type[Serializable], name: str) -> None:
        if self.name is None:
            self.name = name

    def __get__(self, instance: Optional[Serializable],
                owner: Type[Serializable]) -> Any:
        if instance is None:
            return self
        value = None if instance.data is None else instance.data.get(self.name)
        return self.typed(value)

    def __set__(self, instance: Serializable, value: Any) -> None:
        raise AttributeError

    def typed(self, value: Any) -> Any:
        """Cast attribute to specified type"""
        return self.type(value)


@dataclass
class Base64Attribute(Attribute):
    """A data structure Base64-encoded attribute"""

    type: Callable = b64decode

    def typed(self, value: Any) -> Optional[bytes]:
        return None if value is None else self.type(value)


@dataclass
class DateTimeAttribute(Attribute):
    """A data structure datetime attribute"""

    type: Callable = dateutil.parser.parse

    def typed(self, value: Any) -> Optional[datetime]:
        return None if value is None else self.type(value)


@dataclass
class ListAttribute(Attribute):
    """A data structure list attribute"""

    type: Callable = SerializableSequence

    def typed(self, value: Any) -> Sequence:
        return self.type(() if value is None else value)


@dataclass
class DictAttribute(Attribute):
    """A data structure dictionary attribute"""

    type: Callable = SerializableMapping

    def typed(self, value: Any) -> Mapping:
        return self.type({} if value is None else value)
