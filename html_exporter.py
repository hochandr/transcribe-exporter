import base64
import itertools
from datetime import datetime, timedelta
from linque import Linque
from models import XscFile, XscMarker, XscMarkerType, XscColors
from jinja2 import Environment, select_autoescape, FileSystemLoader
import re


def export_to_html(xsc_files: list[XscFile], output_file_path: str):
    songs = []

    for xsc in xsc_files:
        with open(xsc.sound_file.path, 'rb') as binary_file:
            binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_output = base64_encoded_data.decode('utf-8')

        section_markers = Linque(xsc.markers).where(lambda m: m.type == XscMarkerType.Section).to_list()
        regions = _get_regions(section_markers, xsc.sound_file.duration)

        regex = re.compile('[^a-zA-Z]')
        css_id = regex.sub('', xsc.sound_file.name).lower()

        text_blocks = Linque(xsc.text_blocks).where(lambda t: 'Creation date:' not in t.value).select(lambda t: {
            "content": _format_text_block(t.value),
            "timestamp": _format_timestamp(t.timestamp),
            "timestamp_seconds": _get_total_seconds(t.timestamp),
            "color": t.color,
        }).to_list()

        meta_text_block = Linque(xsc.text_blocks).single(lambda t: 'Creation date:' in t.value)
        metadata = meta_text_block.value.replace('\\C', ',').split('\\n')

        songs.append({
            "id": css_id,
            "name": xsc.sound_file.name,
            "base64": base64_output,
            "regions": regions,
            "textblocks": text_blocks,
            "metadata": metadata
        })

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape()
    )
    template = env.get_template('export.html.jinja')

    html = template.render(songs=songs)

    with open(output_file_path, 'wb') as fd:
        fd.write(html.encode(encoding='utf-8'))


def _get_regions(markers: list[XscMarker], sound_file_duration: timedelta) -> object:
    regions = []
    colors = {}
    color_palette = itertools.cycle(XscColors.values())

    for i in range(len(markers)):
        m = markers[i]

        if not m.value:
            continue

        key = m.value.split()[0]
        if key not in colors:
            color = next(color_palette)
            colors[key] = f"rgba({color[0]}, {color[1]}, {color[2]}, 0.66)"

        regions.append({"start": _get_total_seconds(m.timestamp),
                        "end": _get_total_seconds(markers[i + 1].timestamp) if i + 1 < len(
                            markers) else sound_file_duration.total_seconds(),
                        "content": m.value,
                        "color": colors[key]})

    return regions


def _get_total_seconds(d: datetime):
    return (d - datetime(1900, 1, 1)).total_seconds()


def _format_timestamp(d: datetime):
    return d.strftime('%M:%S')


def _format_text_block(t: str):
    return t.replace('\\n', '<br>').replace('\\C', ',')
