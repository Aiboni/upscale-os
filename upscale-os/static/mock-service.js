/* Mock backend service for Upscale OS (iteration 1: frontend works without a server).
 * Enable by opening the app with ?mock=1  — data lives in memory and resets on reload.
 * Mirrors the REST contract in openapi.yml: same paths, status codes and error messages. */
(function () {
  const now = () => new Date().toISOString();
  let seq = { lead: 100, campaign: 100, task: 100, activity: 100 };
  const db = {
    leads: [
      { id: 1, name: 'Olivia Rhye', email: 'olivia@layers.design', company: 'Layers', title: 'VP of Marketing', status: 'Qualified', source: 'LinkedIn', value: 12500, created_at: now() },
      { id: 2, name: 'Phoenix Baker', email: 'phoenix@catalog.io', company: 'Catalog', title: 'Head of Growth', status: 'Contacted', source: 'Email', value: 8400, created_at: now() },
      { id: 3, name: 'Natali Craig', email: 'natali@untitled.ui', company: 'Untitled UI', title: 'Co-Founder', status: 'Won', source: 'LinkedIn', value: 9400, created_at: now() },
    ],
    campaigns: [
      { id: 1, name: 'Mock SaaS Outreach', channel: 'Email', status: 'Active', target: 500, contacted: 200, replies: 30, created_at: now() },
    ],
    tasks: [{ id: 1, title: 'Follow up with Olivia', priority: 'High', done: false, lead_id: null, due_date: null }],
    activities: [{ id: 1, title: 'Mock mode enabled', detail: 'No backend is used', created_at: now() }],
  };
  const STAGES = ['New', 'Contacted', 'Qualified', 'Proposal', 'Won', 'Lost'];
  const fail = (code, msg) => { const e = new Error(msg); e.status = code; throw e; };
  const log = (title, detail) => db.activities.unshift({ id: ++seq.activity, title, detail, created_at: now() });
  const clone = (x) => JSON.parse(JSON.stringify(x));
  const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  function stats() {
    const L = db.leads, C = db.campaigns, T = db.tasks;
    const contacted = C.reduce((a, c) => a + c.contacted, 0), replies = C.reduce((a, c) => a + c.replies, 0);
    return {
      total_leads: L.length, active_campaigns: C.filter(c => c.status === 'Active').length,
      pipeline_value: L.filter(l => l.status !== 'Lost').reduce((a, l) => a + l.value, 0),
      won_value: L.filter(l => l.status === 'Won').reduce((a, l) => a + l.value, 0),
      response_rate: contacted ? Math.round(replies / contacted * 1000) / 10 : 0,
      total_contacted: contacted, total_replies: replies, pending_tasks: T.filter(t => !t.done).length,
      by_status: Object.fromEntries(STAGES.map(s => [s, L.filter(l => l.status === s).length])),
    };
  }

  window.mockApi = async function (path, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    const body = options.body ? JSON.parse(options.body) : {};
    const [route, query = ''] = path.split('?');
    const params = new URLSearchParams(query);
    const [, res, id] = route.split('/');
    const n = Number(id);
    await new Promise(r => setTimeout(r, 60)); // simulate latency

    if (res === 'health') return { status: 'ok', database: 'mock' };
    if (res === 'stats') return stats();
    if (res === 'activities') return clone(db.activities.slice(0, 12));

    if (res === 'leads') {
      if (method === 'GET') {
        const q = (params.get('q') || '').toLowerCase(), st = params.get('status') || '';
        return clone(db.leads.filter(l => (!q || `${l.name} ${l.company} ${l.email}`.toLowerCase().includes(q)) && (!st || l.status === st)));
      }
      if (method === 'POST') {
        if (!body.name || !body.name.trim() || !body.company || !body.company.trim() || !EMAIL.test(body.email || '')) fail(422, 'Invalid lead');
        if (db.leads.some(l => l.email === body.email.toLowerCase())) fail(409, 'This email is already in your CRM');
        const lead = { title: '', status: 'New', source: 'Website', value: 0, ...body, email: body.email.toLowerCase(), id: ++seq.lead, created_at: now() };
        db.leads.unshift(lead); log('New lead added', `${lead.name} · ${lead.company}`); return clone(lead);
      }
      const lead = db.leads.find(l => l.id === n); if (!lead) fail(404, 'Lead not found');
      if (method === 'PATCH') { Object.assign(lead, body); log('Lead updated', `${lead.name} · ${lead.status}`); return clone(lead); }
      if (method === 'DELETE') { db.leads = db.leads.filter(l => l.id !== n); log('Lead deleted', lead.name); return { ok: true }; }
    }
    if (res === 'campaigns') {
      if (method === 'GET') return clone(db.campaigns);
      if (method === 'POST') {
        if (!body.name || !body.name.trim()) fail(422, 'Invalid campaign');
        const c = { channel: 'Email', status: 'Draft', target: 100, contacted: 0, replies: 0, ...body, id: ++seq.campaign, created_at: now() };
        db.campaigns.unshift(c); log('Campaign created', c.name); return clone(c);
      }
      const c = db.campaigns.find(x => x.id === n); if (!c) fail(404, 'Campaign not found');
      if (method === 'PATCH') {
        const next = { ...c, ...body }; if (next.replies > next.contacted) fail(422, 'Replies cannot exceed contacted');
        Object.assign(c, next); log('Campaign updated', `${c.name} · ${c.status}`); return clone(c);
      }
      if (method === 'DELETE') { db.campaigns = db.campaigns.filter(x => x.id !== n); return { ok: true }; }
    }
    if (res === 'tasks') {
      if (method === 'GET') return clone([...db.tasks].sort((a, b) => a.done - b.done || b.id - a.id));
      if (method === 'POST') {
        if (!body.title || !body.title.trim()) fail(422, 'Invalid task');
        const t = { priority: 'Medium', done: false, lead_id: null, due_date: null, ...body, id: ++seq.task };
        db.tasks.unshift(t); log('Task created', t.title); return clone(t);
      }
      const t = db.tasks.find(x => x.id === n); if (!t) fail(404, 'Task not found');
      if (method === 'PATCH') { Object.assign(t, body); return clone(t); }
      if (method === 'DELETE') { db.tasks = db.tasks.filter(x => x.id !== n); return { ok: true }; }
    }
    fail(404, 'Not found');
  };
})();
