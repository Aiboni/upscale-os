from __future__ import annotations
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, ForeignKey, DateTime, Text, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

ROOT = Path(__file__).resolve().parent
DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{ROOT / "upscale.db"}')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass
class Lead(Base):
    __tablename__ = 'leads'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    company: Mapped[str] = mapped_column(String(150))
    title: Mapped[str] = mapped_column(String(150), default='')
    status: Mapped[str] = mapped_column(String(30), default='New')
    source: Mapped[str] = mapped_column(String(60), default='Website')
    value: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
class Campaign(Base):
    __tablename__ = 'campaigns'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    channel: Mapped[str] = mapped_column(String(30), default='Email')
    status: Mapped[str] = mapped_column(String(30), default='Draft')
    target: Mapped[int] = mapped_column(Integer, default=100)
    contacted: Mapped[int] = mapped_column(Integer, default=0)
    replies: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    priority: Mapped[str] = mapped_column(String(20), default='Medium')
    done: Mapped[bool] = mapped_column(default=False)
    lead_id: Mapped[Optional[int]] = mapped_column(ForeignKey('leads.id', ondelete='SET NULL'), nullable=True)
    due_date: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
class Activity(Base):
    __tablename__ = 'activities'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    detail: Mapped[str] = mapped_column(String(250), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

class LeadIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=255)
    company: str = Field(min_length=1, max_length=150)
    title: str = ''
    status: str = 'New'
    source: str = 'Website'
    value: int = Field(default=0, ge=0)
class LeadPatch(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    title: Optional[str] = None
    status: Optional[str] = None
    source: Optional[str] = None
    value: Optional[int] = Field(default=None, ge=0)
class CampaignIn(BaseModel):
    name: str = Field(min_length=1)
    channel: str = 'Email'
    status: str = 'Draft'
    target: int = Field(default=100, ge=1)
class CampaignPatch(BaseModel):
    name: Optional[str] = None
    channel: Optional[str] = None
    status: Optional[str] = None
    target: Optional[int] = Field(default=None, ge=1)
    contacted: Optional[int] = Field(default=None, ge=0)
    replies: Optional[int] = Field(default=None, ge=0)
class TaskIn(BaseModel):
    title: str = Field(min_length=1)
    priority: str = 'Medium'
    due_date: Optional[str] = None
    lead_id: Optional[int] = None
class TaskPatch(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    done: Optional[bool] = None
    due_date: Optional[str] = None

app = FastAPI(title='Upscale OS API', version='1.0.0')
app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')

@app.on_event('startup')
def startup():
    Base.metadata.create_all(engine)
    if os.getenv('SEED_DEMO', '1') == '1':
        seed_demo()

def seed_demo():
    with SessionLocal() as db:
        if db.scalar(select(func.count(Lead.id))) is not None and db.scalar(select(func.count(Lead.id))) > 0:
            return
        leads = [
            ('Olivia Rhye','olivia@layers.design','Layers','VP of Marketing','Qualified','LinkedIn',12500),
            ('Phoenix Baker','phoenix@catalog.io','Catalog','Head of Growth','Contacted','Email',8400),
            ('Lana Steiner','lana@quotient.co','Quotient','CEO & Founder','New','Website',18000),
            ('Demi Wilkinson','demi@sisyphus.com','Sisyphus','Sales Director','Proposal','Email',22000),
            ('Candice Wu','candice@circooles.com','Circooles','CMO','Qualified','Referral',15000),
            ('Natali Craig','natali@untitled.ui','Untitled UI','Co-Founder','Won','LinkedIn',9400),
            ('Drew Cano','drew@cloudline.io','Cloudline','Revenue Operations','New','Website',6800),
            ('Kate Morrison','kate@orbit.so','Orbit','VP of Sales','Contacted','LinkedIn',11200),
        ]
        for name,email,company,title,status,source,value in leads:
            db.add(Lead(name=name,email=email,company=company,title=title,status=status,source=source,value=value))
        db.add_all([
            Campaign(name='Q4 SaaS Founders Outreach',channel='Email',status='Active',target=1200,contacted=846,replies=124),
            Campaign(name='Enterprise Growth Leaders',channel='LinkedIn',status='Active',target=650,contacted=429,replies=68),
            Campaign(name='Agency Partnership Program',channel='Email',status='Paused',target=400,contacted=218,replies=32),
            Campaign(name='October Product Launch',channel='Multi-channel',status='Draft',target=1000,contacted=0,replies=0)
        ])
        db.add_all([
            Task(title='Follow up with Olivia at Layers',priority='High',due_date='2026-10-21'),
            Task(title='Prepare proposal for Sisyphus',priority='High',due_date='2026-10-22'),
            Task(title='Review Q4 outreach messaging',priority='Medium',due_date='2026-10-23'),
            Task(title='Update pipeline forecast',priority='Low',due_date='2026-10-25')
        ])
        db.add_all([
            Activity(title='Deal moved to Won',detail='Natali Craig · Untitled UI'),
            Activity(title='New lead captured',detail='Lana Steiner · Quotient'),
            Activity(title='Campaign performing well',detail='Q4 SaaS Founders Outreach'),
            Activity(title='Proposal sent',detail='Demi Wilkinson · Sisyphus'),
        ])
        db.commit()

def record(db, title, detail):
    db.add(Activity(title=title, detail=detail))

def obj(row, columns):
    result = {key: getattr(row, key) for key in columns}
    for k,v in result.items():
        if isinstance(v,datetime): result[k] = v.isoformat()
    return result
LEAD_KEYS = ['id','name','email','company','title','status','source','value','created_at']
CAMPAIGN_KEYS = ['id','name','channel','status','target','contacted','replies','created_at']
TASK_KEYS = ['id','title','priority','done','due_date','lead_id']

@app.get('/')
def home(): return FileResponse(ROOT/'static'/'index.html')
@app.get('/api/health')
def health(): return {'status':'ok','database':'connected'}
@app.get('/api/leads')
def leads(q: str = '', status: str = ''):
    with SessionLocal() as db:
        rows = db.scalars(select(Lead).order_by(Lead.id.desc())).all()
        return [obj(x,LEAD_KEYS) for x in rows if (not q or q.lower() in f'{x.name} {x.company} {x.email}'.lower()) and (not status or x.status==status)]
@app.post('/api/leads', status_code=201)
def add_lead(data: LeadIn):
    with SessionLocal() as db:
        if db.scalar(select(Lead).where(Lead.email==data.email.lower())): raise HTTPException(409,'This email is already in your CRM')
        x = Lead(**(data.model_dump() | {'email':data.email.lower()}));db.add(x)
        record(db,'New lead added',f'{x.name} · {x.company}');db.commit();db.refresh(x)
        return obj(x,LEAD_KEYS)
@app.patch('/api/leads/{id}')
def edit_lead(id:int,data:LeadPatch):
    with SessionLocal() as db:
        x=db.get(Lead,id)
        if not x: raise HTTPException(404,'Lead not found')
        for k,v in data.model_dump(exclude_unset=True).items(): setattr(x,k,v)
        record(db,'Lead updated',f'{x.name} · {x.status}');db.commit();db.refresh(x)
        return obj(x,LEAD_KEYS)
@app.delete('/api/leads/{id}')
def delete_lead(id:int):
    with SessionLocal() as db:
        x=db.get(Lead,id)
        if not x: raise HTTPException(404,'Lead not found')
        record(db,'Lead deleted',x.name);db.delete(x);db.commit();return {'ok':True}
@app.get('/api/campaigns')
def campaigns():
    with SessionLocal() as db:return [obj(x,CAMPAIGN_KEYS) for x in db.scalars(select(Campaign).order_by(Campaign.id.desc())).all()]
@app.post('/api/campaigns',status_code=201)
def add_campaign(data:CampaignIn):
    with SessionLocal() as db:
        x=Campaign(**data.model_dump());db.add(x);record(db,'Campaign created',x.name);db.commit();db.refresh(x);return obj(x,CAMPAIGN_KEYS)
@app.patch('/api/campaigns/{id}')
def edit_campaign(id:int,data:CampaignPatch):
    with SessionLocal() as db:
        x=db.get(Campaign,id)
        if not x:raise HTTPException(404,'Campaign not found')
        for k,v in data.model_dump(exclude_unset=True).items():setattr(x,k,v)
        record(db,'Campaign updated',f'{x.name} · {x.status}');db.commit();db.refresh(x);return obj(x,CAMPAIGN_KEYS)
@app.delete('/api/campaigns/{id}')
def delete_campaign(id:int):
    with SessionLocal() as db:
        x=db.get(Campaign,id)
        if not x:raise HTTPException(404,'Campaign not found')
        db.delete(x);db.commit();return {'ok':True}
@app.get('/api/tasks')
def tasks():
    with SessionLocal() as db:return [obj(x,TASK_KEYS) for x in db.scalars(select(Task).order_by(Task.done,Task.id.desc())).all()]
@app.post('/api/tasks',status_code=201)
def add_task(data:TaskIn):
    with SessionLocal() as db:
        x=Task(**data.model_dump());db.add(x);record(db,'Task created',x.title);db.commit();db.refresh(x);return obj(x,TASK_KEYS)
@app.patch('/api/tasks/{id}')
def edit_task(id:int,data:TaskPatch):
    with SessionLocal() as db:
        x=db.get(Task,id)
        if not x:raise HTTPException(404,'Task not found')
        for k,v in data.model_dump(exclude_unset=True).items():setattr(x,k,v)
        db.commit();db.refresh(x);return obj(x,TASK_KEYS)
@app.delete('/api/tasks/{id}')
def delete_task(id:int):
    with SessionLocal() as db:
        x=db.get(Task,id)
        if not x:raise HTTPException(404,'Task not found')
        db.delete(x);db.commit();return {'ok':True}
@app.get('/api/activities')
def activities():
    with SessionLocal() as db:return [obj(x,['id','title','detail','created_at']) for x in db.scalars(select(Activity).order_by(Activity.id.desc()).limit(12)).all()]
@app.get('/api/stats')
def stats():
    with SessionLocal() as db:
        ls=db.scalars(select(Lead)).all();cs=db.scalars(select(Campaign)).all();ts=db.scalars(select(Task)).all()
        pipeline=sum(x.value for x in ls if x.status!='Lost')
        won=sum(x.value for x in ls if x.status=='Won')
        contacted=sum(x.contacted for x in cs);replies=sum(x.replies for x in cs)
        return {'total_leads':len(ls),'active_campaigns':sum(x.status=='Active' for x in cs),'pipeline_value':pipeline,'won_value':won,'response_rate':round(replies/contacted*100,1) if contacted else 0,'total_contacted':contacted,'total_replies':replies,'pending_tasks':sum(not t.done for t in ts),'by_status':{s:sum(l.status==s for l in ls) for s in ['New','Contacted','Qualified','Proposal','Won','Lost']}}
