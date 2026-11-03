# Two small edits for `static/index.html` (do these in VS Code, then delete this file)

`index.html` is not overwritten by this patch because your deployed version is newer than the zip (language switcher, revenue selector).

**1. Load the mock service** — before the existing `<script>` tag:
```html
<script src="/static/mock-service.js"></script>
```

**2. Use it when the URL has `?mock=1`, and show validation messages.** Replace the `api` function:
```js
async function api(path,options={}){
  if(location.search.includes('mock=1')) return window.mockApi(path,options);
  let r=await fetch('/api'+path,{headers:{'Content-Type':'application/json'},...options});
  let d=await r.json();
  if(!r.ok){
    const msg=typeof d.detail==='string'?d.detail:Array.isArray(d.detail)?d.detail.map(x=>x.msg).join('; '):'Request failed';
    throw Error(msg);
  }
  return d;
}
```
Test: open `http://127.0.0.1:8000/?mock=1` (works without the database) and `http://127.0.0.1:8000/` (real API).
