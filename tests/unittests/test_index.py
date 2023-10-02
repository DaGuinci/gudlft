def test_index(client):
    response = client.get("/")
    html = response.data.decode()
    assert 'Please enter your secretary email' in html
