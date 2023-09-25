from bs4 import BeautifulSoup

from .conftest import get_points_from_summary


def test_purchasePlaces_should_modify_user_points(client):
    """
    When: a secretary book one ore more places
    Then: the changes are reflected
    """

    purchased_points = 2

    # access to the initial number of points
    response = client.post(
        "/showSummary",
        data={'email': 'admin@irontemple.com'},
        follow_redirects=True
        )
    soup = BeautifulSoup(response.data, 'html.parser')
    initial_points = get_points_from_summary(soup)

    # purchase places
    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': purchased_points
        },
        )
    # access to changed points
    soup = BeautifulSoup(response.data, 'html.parser')
    final_points = get_points_from_summary(soup)

    assert final_points == initial_points - purchased_points
