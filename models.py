import os
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field

XscColors = {
    # "White": (255, 255, 255),
    "Grey": (192, 192, 192),
    # "Black": (0, 0, 0),
    "Red": (255, 128, 128),
    "DarkRed": (128, 0, 0),
    "Green": (128, 255, 128),
    "DarkGreen": (0, 128, 0),
    "Blue": (128, 128, 255),
    "DarkBlue": (0, 0, 128),
    "Teal": (0, 128, 128),
    "Olive": (128, 128, 0),
    "Purple": (128, 0, 128),
    "Cyan": (0, 255, 255),
    "Yellow": (255, 255, 0),
    "Fuchsia": (255, 0, 255),
}


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
