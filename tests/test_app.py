import sys
from pathlib import Path
import pytest
from dash.testing.application_runners import import_app

# 把项目根目录加入 Python import 路径，确保能 import app.py
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def app():
    return import_app("app")  # app.py


def test_header_present(dash_duo, app):
    dash_duo.start_server(app)
    header = dash_duo.find_element("h1")
    assert "Impact of Pink Morsel Price Increase on Sales" in header.text


def test_visualisation_present(dash_duo, app):
    dash_duo.start_server(app)
    graph = dash_duo.find_element("#sales-chart")
    assert graph is not None


def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    radio = dash_duo.find_element("#region-filter")
    assert radio is not None