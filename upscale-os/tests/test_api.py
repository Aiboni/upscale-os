import os
import tempfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Test against an isolated SQLite database, no seeded content.
tmp = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(tmp.name) / 'test.db')
os.environ['SEED_DEMO'] = '0'
from fastapi.testclient import TestClient
from app import app, Base, engine


def test_crm_roundtrip():
    with TestClient(app) as client:
        assert client.get('/api/health').json()['status'] == 'ok'
        lead = client.post('/api/leads',json={'name':'Alice','email':'alice@test.com','company':'Acme','value':4500})
        assert lead.status_code == 201
        lid = lead.json()['id']
        assert client.post('/api/leads',json={'name':'Alice','email':'alice@test.com','company':'Acme'}).status_code == 409
        assert len(client.get('/api/leads?q=Acme').json()) == 1
        assert client.patch(f'/api/leads/{lid}',json={'status':'Qualified'}).json()['status'] == 'Qualified'
        assert client.get('/api/stats').json()['pipeline_value'] == 4500
        camp = client.post('/api/campaigns',json={'name':'SaaS outreach','target':100}).json()
        assert client.patch(f'/api/campaigns/{camp["id"]}',json={'status':'Active','contacted':50,'replies':10}).json()['replies'] == 10
        assert client.get('/api/stats').json()['response_rate'] == 20.0
        task = client.post('/api/tasks',json={'title':'Call Alice'}).json()
        assert client.patch(f'/api/tasks/{task["id"]}',json={'done':True}).json()['done'] is True
        assert client.delete(f'/api/tasks/{task["id"]}').status_code == 200
        assert client.delete(f'/api/campaigns/{camp["id"]}').status_code == 200
        assert client.delete(f'/api/leads/{lid}').status_code == 200
        assert client.patch('/api/leads/9999',json={'status':'Won'}).status_code == 404
        assert len(client.get('/api/activities').json()) > 0

def test_frontend_and_schema():
    with TestClient(app) as client:
        page=client.get('/')
        assert page.status_code == 200
        assert 'Upscale OS' in page.text
        assert client.get('/openapi.json').status_code == 200
