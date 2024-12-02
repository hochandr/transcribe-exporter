from datetime import datetime, timedelta

from linque import Linque
from pathlib import Path, PureWindowsPath

from models import XscMarker, XscTextBlock, XscLoop, XscMarkerType, XscSoundFile

datetime_format = '%H:%M:%S.%f'


def parse_markers(section):
    for marker in section[2:len(section) - 1]:
        yield XscMarker(marker[3], datetime.strptime(marker[5], datetime_format), XscMarkerType(marker[0]))


def parse_text_blocks(section):
    for text_block in section[3:len(section) - 1]:
        yield XscTextBlock(text_block[6], datetime.strptime(text_block[5], datetime_format), text_block[4])


def parse_loops(section):
    for loop in section[2:len(section) - 1]:
        duration_dt = datetime.strptime(loop[9], datetime_format)
        duration_td = timedelta(hours=duration_dt.hour, minutes=duration_dt.minute, seconds=duration_dt.second,
                                microseconds=duration_dt.microsecond)

        if duration_td.total_seconds() == 0:
            continue
        yield XscLoop(loop[5], datetime.strptime(loop[8], datetime_format), loop[6], duration_td)


def parse_main(section):
    duration_secs = Linque(section).where(lambda l: l[0] == 'SoundFileInfo').select(
        lambda l: float(l[len(l) - 1])).single()
    path = Linque(section).where(lambda l: l[0] == 'SoundFileName').select(
        lambda l: l[len(l) - 1]).single()
    platform = Linque(section).where(lambda l: l[0] == 'SoundFileName').select(
        lambda l: l[len(l) - 2]).single()
    name = PureWindowsPath(path) if platform == 'Win' else Path(path)

    return XscSoundFile(name.stem, timedelta(seconds=duration_secs), path)
