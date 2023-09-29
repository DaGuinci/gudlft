def test_board_should_display_clubs_points(client):
    """
    when: a secratary try to book more than the club's current points
    then: the app flashes an error message
    """

    # purchase places
    response = client.get("/board")

    assert ('Table of club\'s points:' in
            response.data.decode())
