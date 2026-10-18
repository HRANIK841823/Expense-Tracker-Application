from fastapi.testclient import TestClient
from main import app
from router.auth import get_current_user
from fastapi import status
from models import Transactions

#===============================
#     Bypass Authentication
#===============================
def override_get_current_user():
    return{
        "id":1,
        "username":"testuser"
    }
app.dependency_overrides[get_current_user]=override_get_current_user

#===============================
# Connection with app
#===============================
client=TestClient(app)

#===============================
# Get Transaction Test
#===============================
def test_get_transactions():
    response=client.get('/transactions')
    assert response.status_code==status.HTTP_200_OK

#===============================
# Create Transactions Test
#===============================
def test_created_transactions():
    response=client.post('/transactions',json={
        "title":"MIAM Tution",
        "amount":"90000",
        "type":"income",
        "category":"Tution Payment",
    })
    
    assert response.status_code==status.HTTP_201_CREATED

#===============================
# Get Specific Transaction Test
#===============================
def test_specific_transactions():
    response=client.get('/transactions/4')
    assert response.status_code==status.HTTP_200_OK


#===============================
# Edit Transactions test
#===============================
def test_update_transactions():
    response=client.put('/transactions/4',json={
        "amount":"9000"
       
    })

    assert response.status_code==status.HTTP_200_OK
    assert response.json()=={'message':"Transaction Updated Successfully"}

#===============================
# Delete Transactions test
#===============================
def test_delete_transactions():
    response=client.delete('/transactions/4')
    assert response.status_code==status.HTTP_200_OK







