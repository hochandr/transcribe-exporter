import os
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field


class XscMarkerType(Enum):
    Section = 'S'
    Measure = 'M'
    Beat = 'B'


@dataclass
class XscElement:
    value: str
    timestamp: datetime


@dataclass
class XscMarker(XscElement):
    type: XscMarkerType


@dataclass
class XscTextBlock(XscElement):
    color: str


@dataclass
class XscLoop(XscElement):
    color: str
    duration: timedelta


@dataclass
class XscSoundFile:
    name: str
    duration: timedelta
    path: os.PathLike


@dataclass
class XscFile:
    sound_file: XscSoundFile = XscSoundFile
    markers: list[XscMarker] = field(default_factory=list)
    text_blocks: list[XscTextBlock] = field(default_factory=list)
    loops: list[XscLoop] = field(default_factory=list)
