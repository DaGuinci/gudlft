from bs4 import BeautifulSoup

from tests.conftest import get_points_from_summary


def test_login_purchase_get_board_logout(client):
    # the user visit the login page
    response = client.get("/")
    assert 'Please enter your secretary email' in response.data.decode()

    # then he logs in
    response = client.post(
        "/showSummary",
        data={'email': 'test@clubtest.com'},
        follow_redirects=True
        )
    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'Welcome, test@clubtest.com' in response.data.decode()

    # he can see his available points
    initial_points = get_points_from_summary(soup)  # 13
    assert initial_points == 13

    # he visits the purchase places page
    competition_link = soup.find_all('li')[0].find('a').get('href')
    response = client.get(competition_link)
    assert '<h2>Competition test</h2>' in response.data.decode()

    # he purchases 2 places
    response = client.post(
        "/purchasePlaces",
        data={
            'club': 'Club test',
            'competition': 'Competition test',
            'places': 2
        },
        )
    assert 'Great-booking complete!' in response.data.decode()

    # he wants to see the available points board
    soup = BeautifulSoup(response.data, 'html.parser')
    board_link = soup.find_all('a')[-1].get('href')
    response = client.get(board_link)
    assert '<h3>Table of club\'s points:</h3>' in response.data.decode()

    # to log out, he goes back
    response = client.post(
        "/showSummary",
        data={'email': 'test@clubtest.com'},
        follow_redirects=True
        )
    soup = BeautifulSoup(response.data, 'html.parser')
    logout_link = soup.find('a').get('href')
    response = client.get(logout_link, follow_redirects=True)
    soup = BeautifulSoup(response.data, 'html.parser')
    assert 'GUDLFT Registration' == soup.title.text
