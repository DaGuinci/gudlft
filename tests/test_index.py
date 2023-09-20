def test_index(client):
    landing = client.get("/")
    html = landing.data.decode()
    assert 'Welcome' in html