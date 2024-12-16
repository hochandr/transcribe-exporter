import logging as logger

from html_exporter import export_to_html
from parser import parse_transcribe_file


def main(transcribe_file_paths: str, filter_textblocks: str):
    xsc_files = []

    for path in transcribe_file_paths:
        xsc = parse_transcribe_file(path)
        xsc_files.append(xsc)

    export_to_html(xsc_files, filter_textblocks, "export.html")

    logger.info(f"Successfully exported '{transcribe_file_paths}'")


if __name__ == '__main__':
    logger.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logger.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='')
    parser.add_argument('--paths', '-p', help='Paths to Transcribe! files',
                        default=[
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Weezer - Say it ain't so\\transcriptions\\Weezer - Say it ain't so.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\FIBEL - Ehrlichkeit\\transcriptions\\FIBEL - Ehrlichkeit.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Queens of the Stone Age - The Lost Art of Keeping a Secret\\transcriptions\\Queens of the Stone Age - The Lost Art of Keeping a Secret.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Kashmir - Kalifornia\\transcriptions\\Kashmir - Kalifornia.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Arctic Monkeys - When the sun goes down\\transcriptions\\Arctic Monkeys - When the sun goes down.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Incubus - Wish you were here\\transcriptions\\Incubus - Wish you were here.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Incubus - Anna Molly\\transcriptions\\Incubus - Anna Molly.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Audioslave - Like a stone\\transcriptions\\Audioslave - Like a stone.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Green Day - Longview\\transcriptions\\Green Day - Longview.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Pearl Jam - Do the evolution\\transcriptions\\Pearl Jam - Do the evolution.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Red Hot Chili Peppers - Suck my kiss\\transcriptions\\Red Hot Chili Peppers - Suck my kiss.xsc",
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\Audioslave - Be yourself\\transcriptions\\Audioslave - Be yourself.xsc", 
                                    "C:\\Users\\Andreas\\Documents\\Gitarre\\Repertoire\\The Cardigans - My Favourite Game\\transcriptions\\The Cardigans - My Favourite Game.xsc"
                                 ])
    parser.add_argument('--filter-textblocks', '-ft', help='Include filter for textblocks', default=['Beide', 'AH', 'RJ'])
    args = parser.parse_args()
    main(args.paths, args.filter_textblocks)
