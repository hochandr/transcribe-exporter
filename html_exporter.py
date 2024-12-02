import base64
from datetime import datetime, timedelta
import random
from linque import Linque
from models import XscFile, XscMarker, XscMarkerType
from jinja2 import Environment, select_autoescape, FileSystemLoader


def export_to_html(xsc: XscFile):
    with open(xsc.sound_file.path, 'rb') as binary_file:
        binary_file_data = binary_file.read()
    base64_encoded_data = base64.b64encode(binary_file_data)
    base64_output = base64_encoded_data.decode('utf-8')

    section_markers = Linque(xsc.markers).where(lambda m: m.type == XscMarkerType.Section).to_list()
    regions = get_regions(section_markers, xsc.sound_file.duration)

    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape()
    )
    env.filters['totalSeconds'] = get_total_seconds
    env.filters['formatTimestamp'] = format_timestamp
    template = env.get_template('export.html.jinja')

    return template.render(xsc=xsc, base64=base64_output, regions=regions)


def get_regions(markers: list[XscMarker], sound_file_duration: timedelta) -> object:
    regions = []
    colors = {}

    for i in range(len(markers)):
        m = markers[i]

        if not m.value:
            continue

        key = m.value.split()[0]
        if key not in colors:
            colors[key] = get_random_color()

        regions.append({"start": get_total_seconds(m.timestamp),
                        "end": get_total_seconds(markers[i + 1].timestamp) if i + 1 < len(
                            markers) else sound_file_duration.total_seconds(),
                        "content": m.value,
                        "color": colors[key]})

    return regions


def get_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return f"rgba({r}, {g}, {b}, 0.5)"


def get_total_seconds(d: datetime):
    return (d - datetime(1900, 1, 1)).total_seconds()


def format_timestamp(d: datetime):
    return d.strftime('%M:%S')
