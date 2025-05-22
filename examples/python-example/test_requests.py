import requests

def test_requests():
    response = requests.get('https://httpbin.org/get')
    assert response.status_code == 200
    assert 'url' in response.json() 