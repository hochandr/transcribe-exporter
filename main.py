import logging as logger

from html_exporter import export_to_html
from parser import parse_transcribe_file


def main(transcribe_file_paths: str):
    xsc_files = []

    for path in transcribe_file_paths:
        xsc = parse_transcribe_file(path)
        xsc_files.append(xsc)

    export_to_html(xsc_files, "transcribe.html")

    logger.info(f"Successfully exported '{transcribe_file_paths}'")


if __name__ == '__main__':
    logger.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logger.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='')
    parser.add_argument('--paths', '-p', help='Paths to Transcribe! files',
                        default=['/home/ahoch/Desktop/FIBEL - Ehrlichkeit.xsc',
                                 '/home/ahoch/Desktop/The Cardigans - My Favourite Game.xsc'])
    args = parser.parse_args()
    main(args.paths)
