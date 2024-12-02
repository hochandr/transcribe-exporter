import csv
import itertools
import logging as logger
from linque import Linque

from html_exporter import export_to_html
from models import XscFile
from parser import parse_markers, parse_text_blocks, parse_loops, parse_main


def main(transcribe_file_path: str, standalone: bool):
    with open(transcribe_file_path, mode='r', ) as file:
        xsc_file = csv.reader(file)
        content = Linque(xsc_file).to_list()
    sections = [list(y) for x, y in itertools.groupby(content, lambda z: len(z) == 0) if not x]

    xsc = XscFile()

    for section in sections:
        section_type = section[0][0] if len(section[0]) < 2 else section[0][1]
        match section_type:
            case 'Main':
                xsc.sound_file = parse_main(section)
            case 'Markers':
                xsc.markers = parse_markers(section)
            case 'Loops':
                xsc.loops = parse_loops(section)
            case 'TextBlocks':
                xsc.text_blocks = parse_text_blocks(section)
            case _:
                logger.debug(f"Skipping '{section_type}' section")

    html = export_to_html(xsc)

    with open(f"{xsc.sound_file.name}.html", 'wb') as fd:
        fd.write(html.encode(encoding='utf-8'))

    logger.info(f"Successfully exported '{xsc.sound_file.name}'")


if __name__ == '__main__':
    logger.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logger.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='')
    parser.add_argument('--path', '-p', help='Path to Transcribe! file',
                        default='/home/ahoch/Desktop/FIBEL - Ehrlichkeit.xsc')
    parser.add_argument('--standalone', '-s', help='Packs all required files in a zip archive',
                        default='false')
    args = parser.parse_args()
    main(args.path, args.standalone)
