"""Apply the two small edits from _docs/frontend-patch.md to static/index.html (safe to run twice)."""
from pathlib import Path
import sys

p = Path('static/index.html')
s = p.read_text(encoding='utf-8')
OLD = "async function api(path,options={}){let r=await fetch('/api'+path,{headers:{'Content-Type':'application/json'},...options});let d=await r.json();if(!r.ok)throw Error(typeof d.detail==='string'?d.detail:'Request failed');return d}"
NEW = ("async function api(path,options={}){if(location.search.includes('mock=1'))return window.mockApi(path,options);"
       "let r=await fetch('/api'+path,{headers:{'Content-Type':'application/json'},...options});let d=await r.json();"
       "if(!r.ok){const msg=typeof d.detail==='string'?d.detail:Array.isArray(d.detail)?d.detail.map(x=>x.msg).join('; '):'Request failed';throw Error(msg)}return d}")
TAG = '<script src="/static/mock-service.js"></script>\n'
changed = False
if 'mock-service.js' not in s:
    s = s.replace('<script>', TAG + '<script>', 1); changed = True
if 'window.mockApi' not in s:
    if OLD not in s:
        sys.exit('api() function differs from the expected text - edit it by hand using _docs/frontend-patch.md')
    s = s.replace(OLD, NEW, 1); changed = True
if changed:
    p.write_text(s, encoding='utf-8'); print('index.html patched')
else:
    print('index.html already patched')
