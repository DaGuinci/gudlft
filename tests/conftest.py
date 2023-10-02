import pytest
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

    server.app.config['TESTING'] = True
    return server.app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clubs(monkeypatch):
    mock_clubs = [
        {"name": "Club test", "email": "test@clubtest.com", "points": "13"},
        {"name": "Club test 2", "email": "test@clubtest2.com", "points": "4"},
    ]
    monkeypatch.setattr(server, "clubs", mock_clubs)


@pytest.fixture(scope="function", autouse=True)
def competitions(monkeypatch):
    mock_competitions = [
        {
            "name": "Competition test",
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "8"
        },
        {
            "name": "Competition test 2",
            "date": "2021-10-22 13:30:00",
            "numberOfPlaces": "8"
        }
    ]
    monkeypatch.setattr(server, "competitions", mock_competitions)


def get_points_from_summary(html):
    content = html.body.text

    for line in content.splitlines():
        if 'Points available' in line:
            # delete all but number of points
            points = line[22:]
            if points.isdigit():
                points = int(points)
    return points
