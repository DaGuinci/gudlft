def test_showSummary_should_prompt_error_message(client):
    """
    When: the given email isn't in database
    Then: the page redirect to index with error message
    """
    response = client.post(
        "/showSummary",
        data={'email': 'error@test.com'},
        follow_redirects=True
        )
    assert 'Email not found' in response.data.decode()


def test_showSummary_should_redirect_to_app(client):
    """
    When: the given email is in database
    Then: the page redirect to the welcome page
    """
    response = client.post(
        "/showSummary",
        data={'email': 'admin@irontemple.com'},
        follow_redirects=True
        )
    assert 'Welcome, admin@irontemple.com' in response.data.decode()
