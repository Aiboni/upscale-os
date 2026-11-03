"""Regression tests for input validation and error paths (see _docs/issues-groomed.md)."""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if 'app' not in sys.modules:  # keep an isolated, unseeded DB when this file runs alone
    _tmp = tempfile.mkdtemp()
    os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(_tmp) / 'validation.db')
    os.environ['SEED_DEMO'] = '0'

import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def make_lead(client, email, **extra):
    r = client.post('/api/leads', json={'name': 'Test User', 'email': email, 'company': 'TestCo', **extra})
    assert r.status_code == 201, r.text
    return r.json()['id']


# ---- Leads -----------------------------------------------------------------
@pytest.mark.parametrize('email', ['abc', 'a@b', '@x.com', 'a b@x.com', ''])
def test_lead_rejects_invalid_email(client, email):
    r = client.post('/api/leads', json={'name': 'X', 'email': email, 'company': 'Y'})
    assert r.status_code == 422


@pytest.mark.parametrize('field', ['name', 'company'])
def test_lead_rejects_blank_required_text(client, field):
    body = {'name': 'X', 'email': 'blank@test.com', 'company': 'Y', field: '   '}
    assert client.post('/api/leads', json=body).status_code == 422


def test_lead_rejects_negative_value_and_unknown_stage(client):
    base = {'name': 'X', 'email': 'neg@test.com', 'company': 'Y'}
    assert client.post('/api/leads', json={**base, 'value': -1}).status_code == 422
    assert client.post('/api/leads', json={**base, 'status': 'Hacked'}).status_code == 422
    assert client.post('/api/leads', json={**base, 'source': 'Telepathy'}).status_code == 422


def test_lead_patch_validation_and_missing_id(client):
    lid = make_lead(client, 'patch@test.com')
    try:
        assert client.patch(f'/api/leads/{lid}', json={'status': 'Hacked'}).status_code == 422
        assert client.patch(f'/api/leads/{lid}', json={'name': ''}).status_code == 422
        assert client.patch(f'/api/leads/{lid}', json={'value': -5}).status_code == 422
        assert client.patch(f'/api/leads/{lid}', json={'status': 'Won'}).json()['status'] == 'Won'
    finally:
        client.delete(f'/api/leads/{lid}')
    assert client.delete('/api/leads/987654').status_code == 404


def test_lead_email_is_case_insensitive_duplicate(client):
    lid = make_lead(client, 'case@test.com')
    try:
        dup = client.post('/api/leads', json={'name': 'B', 'email': 'CASE@Test.com', 'company': 'C'})
        assert dup.status_code == 409
    finally:
        client.delete(f'/api/leads/{lid}')


def test_lead_status_filter_and_search(client):
    lid = make_lead(client, 'filter@test.com', status='Won', company='FilterCorp')
    try:
        won = client.get('/api/leads?status=Won&q=FilterCorp').json()
        assert [x['id'] for x in won] == [lid]
        assert client.get('/api/leads?status=New&q=FilterCorp').json() == []
    finally:
        client.delete(f'/api/leads/{lid}')


# ---- Campaigns ---------------------------------------------------------------
def test_campaign_validation_and_replies_rule(client):
    assert client.post('/api/campaigns', json={'name': ''}).status_code == 422
    assert client.post('/api/campaigns', json={'name': 'X', 'target': 0}).status_code == 422
    assert client.post('/api/campaigns', json={'name': 'X', 'status': 'Flying'}).status_code == 422
    cid = client.post('/api/campaigns', json={'name': 'Reg', 'target': 10}).json()['id']
    try:
        assert client.patch(f'/api/campaigns/{cid}', json={'contacted': 5, 'replies': 9}).status_code == 422
        untouched = [c for c in client.get('/api/campaigns').json() if c['id'] == cid][0]
        assert (untouched['contacted'], untouched['replies']) == (0, 0)  # rejected update not saved
        ok = client.patch(f'/api/campaigns/{cid}', json={'contacted': 5, 'replies': 2})
        assert ok.status_code == 200 and ok.json()['replies'] == 2
    finally:
        client.delete(f'/api/campaigns/{cid}')


def test_campaign_missing_id(client):
    assert client.patch('/api/campaigns/987654', json={'status': 'Active'}).status_code == 404
    assert client.delete('/api/campaigns/987654').status_code == 404


# ---- Tasks -------------------------------------------------------------------
def test_task_validation_and_missing_id(client):
    assert client.post('/api/tasks', json={'title': '   '}).status_code == 422
    assert client.post('/api/tasks', json={'title': 'x', 'priority': 'Urgent'}).status_code == 422
    assert client.patch('/api/tasks/987654', json={'done': True}).status_code == 404
    assert client.delete('/api/tasks/987654').status_code == 404


def test_task_complete_changes_pending_count(client):
    before = client.get('/api/stats').json()['pending_tasks']
    tid = client.post('/api/tasks', json={'title': 'Pending check'}).json()['id']
    try:
        assert client.get('/api/stats').json()['pending_tasks'] == before + 1
        client.patch(f'/api/tasks/{tid}', json={'done': True})
        assert client.get('/api/stats').json()['pending_tasks'] == before
    finally:
        client.delete(f'/api/tasks/{tid}')


# ---- Misc --------------------------------------------------------------------
def test_stats_shape_and_activity_limit(client):
    stats = client.get('/api/stats').json()
    for key in ['total_leads', 'pipeline_value', 'won_value', 'response_rate', 'by_status']:
        assert key in stats
    assert len(client.get('/api/activities').json()) <= 12

