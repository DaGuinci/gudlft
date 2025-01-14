import html
from bs4 import BeautifulSoup

from tests.conftest import get_points_from_summary


def test_purchasePlaces_should_modify_user_points(
        client,
        ):
    """
    When: a secretary book one or more places
    Then: the places are booked and the changes are reflected
    """
    purchased_points = 2
    response = client.post(
        "/showSummary",
        data={'email': 'test@clubtest.com'},
        follow_redirects=True
        )
    soup = BeautifulSoup(response.data, 'html.parser')

    initial_points = get_points_from_summary(soup)  # 13

    # purchase places in a future competition
    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test',
            'competition': 'Competition test',
            'places': purchased_points
        },
        )
    # access to changed points
    soup = BeautifulSoup(response.data, 'html.parser')
    final_points = get_points_from_summary(soup)  # 2
    assert 'Great-booking complete!' in response.data.decode()
    assert final_points == initial_points - purchased_points


def test_purchasePlaces_should_not_allow_spend_more_than_available(client):
    """
    when: a secratary tries to book more than the club's current points
    then: the app flashes an error message
    """
    purchased_points = 6

    # purchase places
    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test 2',
            'competition': 'Competition test',
            'places': purchased_points
        },
        )
    assert (
        "You can't spend more points than you have." in
        html.unescape(response.data.decode())
        )


def test_shouldnt_book_more_than_twelve_places(
        client,
        ):
    """
    when: a secratary tries to book more than 12 places
    then: the app flashes an error message
    """
    purchased_points = 13

    # purchase places in a future competition
    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test',
            'competition': 'Competition test',
            'places': purchased_points
        },
        )

    assert (
        "You can\'t book more than 12 places in a competition." in
        html.unescape(response.data.decode())
        )


def test_chouldnt_be_able_to_book_for_past_competition(
        client
        ):
    """
    when: a secratary tries to book places in a past competition
    then: the app flashes an error message
    """
    purchased_points = 4

    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test',
            'competition': 'Competition test 2',
            'places': purchased_points
        },
        )

    assert (
        "You can\'t book any place in a past competition." in
        html.unescape(response.data.decode())
        )


def test_chouldnt_be_able_to_book_more_places_than_available(
        client
        ):
    """
    when: a secratary tries to book more places than available in competition
    then: the app flashes an error message
    """
    purchased_points = 9

    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test',
            'competition': 'Competition test',
            'places': purchased_points
        },
        )

    assert (
        "There aren\'t enough places available in this competition." in
        html.unescape(response.data.decode())
        )
