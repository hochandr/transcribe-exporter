import os
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field

XscColors = {
    "DarkGreen": (0, 128, 0),
    "DarkRed": (128, 0, 0),
    "Fuchsia": (255, 0, 255),
    "DarkBlue": (0, 0, 128),
    "Purple": (128, 0, 128),
    "Cyan": (0, 255, 255),
    "Yellow": (255, 255, 0),
    "Teal": (0, 128, 128),
    "Olive": (128, 128, 0),
    "Red": (255, 128, 128),
    "Green": (128, 255, 128),
    "Blue": (128, 128, 255),
    # "Black": (0, 0, 0),
    # "White": (255, 255, 255),
    "Grey": (192, 192, 192),
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
