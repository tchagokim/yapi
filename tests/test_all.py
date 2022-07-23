from fastapi.testclient import TestClient
import pytest

from main import app, models

models_list =  [f"/{model.__name__.lower().strip()}" for model in models]

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"health": "ok"}

@pytest.mark.parametrize('path',models_list)
def test_get_router(path):
    response = client.get(path)
    assert response.status_code == 200


@pytest.mark.parametrize('path', models_list)
def test_get_id_1_router(path):
    path_ = path + "/1"
    response = client.get(path_)
    assert response.status_code == 200
    
    
