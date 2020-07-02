from app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_maps(client):
    response = client.get('/maps')
    assert response.status_code == 200


def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200


def test_about_map(client):
    response = client.get('/about-map')
    assert response.status_code == 200


def test_develop_by(client):
    response = client.get('/accreditation')
    assert response.status_code == 200


def test_objectives(client):
    response = client.get('/objectives')
    assert response.status_code == 200


def test_resources(client):
    response = client.get('/resources')
    assert response.status_code == 302


def test_termsofserviceces(client):
    response = client.get('/termsofservice')
    assert response.status_code == 200


def test_privacypolicy(client):
    response = client.get('/privacypolicy')
    assert response.status_code == 200
