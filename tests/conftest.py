import pytest
from ..server import app


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


def get_points_from_summary(html):
    content = html.body.text

    for line in content.splitlines():
        if 'Points available' in line:
            print(line)
            # delete all but number of points
            points = line[22:]
            if points.isdigit():
                points = int(points)
    return points
