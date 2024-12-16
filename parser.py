from datetime import datetime, timedelta
import csv
import itertools
from linque import Linque
from pathlib import Path, PureWindowsPath
import logging as logger

from models import XscMarker, XscTextBlock, XscLoop, XscMarkerType, XscSoundFile, XscFile

datetime_format = '%H:%M:%S.%f'


def parse_transcribe_file(file_path: str) -> XscFile:
    with open(file_path, mode='r', encoding='utf-8') as file:
        xsc_file = csv.reader(file)
        content = Linque(xsc_file).to_list()
    sections = [list(y) for x, y in itertools.groupby(content, lambda z: len(z) == 0) if not x]

    xsc = XscFile()

    for section in sections:
        section_type = section[0][0] if len(section[0]) < 2 else section[0][1]
        match section_type:
            case 'Main':
                xsc.sound_file = _parse_main(section)
            case 'Markers':
                xsc.markers = _parse_markers(section)
            case 'Loops':
                xsc.loops = _parse_loops(section)
            case 'TextBlocks':
                xsc.text_blocks = _parse_text_blocks(section)
            case _:
                logger.debug(f"Skipping '{section_type}' section")

    return xsc


def _parse_markers(section):
    for marker in section[2:len(section) - 1]:
        marker = _unescape(marker);
        yield XscMarker(marker[3], datetime.strptime(marker[5], datetime_format), XscMarkerType(marker[0]))


def _parse_text_blocks(section):
    text_blocks = []
    for text_block in section[3:len(section) - 1]:
        text_block = _unescape(text_block);
        text_blocks.append(
            XscTextBlock(text_block[6], datetime.strptime(text_block[5], datetime_format), text_block[4]))
    return text_blocks


def _parse_loops(section):
    for loop in section[2:len(section) - 1]:
        loop = _unescape(loop)
        duration_dt = datetime.strptime(loop[9], datetime_format)
        duration_td = timedelta(hours=duration_dt.hour, minutes=duration_dt.minute, seconds=duration_dt.second,
                                microseconds=duration_dt.microsecond)

        if duration_td.total_seconds() == 0:
            continue
        yield XscLoop(loop[5], datetime.strptime(loop[8], datetime_format), loop[6], duration_td)


def _parse_main(section):
    duration_secs = Linque(section).where(lambda l: l[0] == 'SoundFileInfo').select(
        lambda l: float(l[len(l) - 1])).single()
    path = Linque(section).where(lambda l: l[0] == 'SoundFileName').select(
        lambda l: l[len(l) - 1]).single()
    platform = Linque(section).where(lambda l: l[0] == 'SoundFileName').select(
        lambda l: l[len(l) - 2]).single()
    name = PureWindowsPath(path) if platform == 'Win' else Path(path)

    return XscSoundFile(name.stem, timedelta(seconds=duration_secs), path)

def _unescape(x: list[str]):
    return Linque(x).select(lambda l: l.replace('\\C', ',')).to_list();
