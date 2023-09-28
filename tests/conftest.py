import pytest
from ..server import app
import server

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def setup_app(app):
    app.competitions = mocked_competitions


def mocked_competitions():
    competitions = [
        {
            'name': 'future_competition',
            'date': '2023-12-24 09:00:00',
            'numberOfPlaces': 25
        }
    ]
    return competitions


def get_points_from_summary(html):
    content = html.body.text

    for line in content.splitlines():
        if 'Points available' in line:
            # delete all but number of points
            points = line[22:]
            if points.isdigit():
                points = int(points)
    return points
