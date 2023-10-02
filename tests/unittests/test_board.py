def test_board_should_display_clubs_points(client):
    """
    when: any user tries to see the points statement board
    then: the app displays the board
    """

    # purchase places
    response = client.get("/board")

    assert ('Table of club\'s points:' in
            response.data.decode())
