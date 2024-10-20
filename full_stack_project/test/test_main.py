from .utils import *

# Create test 
def test_main():

    # client request
    response = client.get('/healthy')

    assert response.status_code == 200
    assert response.json() == {"status":"Healthy"}

