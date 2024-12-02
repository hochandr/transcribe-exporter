from models import XscFile
from jinja2 import Environment, select_autoescape, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(),
)


def export_to_html(xsc: XscFile):
    template = env.get_template('export.html.jinja')
    return template.render(xsc=xsc)
