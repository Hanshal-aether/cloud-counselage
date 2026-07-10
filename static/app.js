// ── State ─────────────────────────────────────────────────────
let sessionId = 'web_' + Math.random().toString(36).substr(2, 9);
let currentChannel = 'web';
let msgCount = 0;
let editingFaqId = null;
let allFaqs = [];

const platformThemes = {
  web:       { theme: '',                  label: '🌐 Web Chat',   emoji: '🌐' },
  telegram:  { theme: 'theme-telegram',    label: '✈️ Telegram',   emoji: '✈️' },
  whatsapp:  { theme: 'theme-whatsapp',    label: '📱 WhatsApp',   emoji: '📱' },
  messenger: { theme: 'theme-messenger',   label: '💬 Messenger',  emoji: '💬' },
  instagram: { theme: 'theme-instagram',   label: '📸 Instagram',  emoji: '📸' },
};

// Init
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('session-display').textContent = sessionId.substr(0, 14) + '...';
  updateMsgCount();
});

// ── Navigation ─────────────────────────────────────────────────
const pageMeta = {
  chat:      { title: 'Web Chat',     sub: 'AI-powered student support' },
  dashboard: { title: 'Dashboard',    sub: 'Analytics & performance' },
  faqs:      { title: 'FAQ Manager',  sub: 'Manage the knowledge base' },
};

function navigate(page) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  // Show target page
  const target = document.getElementById('page-' + page);
  if (target) target.classList.add('active');
  // Update nav active state
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const navEl = document.querySelector(`.nav-item[data-page="${page}"]`);
  if (navEl) navEl.classList.add('active');
  // Update topbar
  if (pageMeta[page]) {
    document.getElementById('page-title').textContent = pageMeta[page].title;
    document.getElementById('page-sub').textContent = pageMeta[page].sub;
  }
  // Load data for page
  if (page === 'dashboard') loadDashboard();
  if (page === 'faqs') loadFAQs();
}

// ── Channel Switch ─────────────────────────────────────────────
function switchChannel(channel, el) {
  currentChannel = channel;
  const info = platformThemes[channel];

  // Remove all themes
  document.body.className = info.theme;

  // Update active chip
  document.querySelectorAll('.ch-chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');

  // Update header label
  document.getElementById('platform-label').textContent = info.label;
  document.getElementById('current-channel-val').textContent = info.label;

  // Update chat placeholder
  document.getElementById('chat-input').placeholder = `Message on ${info.label}...`;

  // Show platform switch message in chat
  addMsg(`Switched to ${info.label} mode. Messages will be tracked as ${channel} channel.`, 'bot', null);
}

// ── Chat ───────────────────────────────────────────────────────
function addMsg(text, role, tag) {
  const container = document.getElementById('messages');
  const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  const div = document.createElement('div');
  div.className = `msg ${role}`;
  div.innerHTML = `
    <div class="msg-bubble">${escHtml(text)}</div>
    <div class="msg-meta">
      ${tag ? `<span class="msg-tag ${tag === 'faq' ? 'tag-faq' : 'tag-ai'}">${tag === 'faq' ? '✓ Knowledge base' : '✦ AI generated'}</span>` : ''}
      <span class="msg-time">${now}</span>
    </div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  msgCount++;
  updateMsgCount();
}

function updateMsgCount() {
  const el = document.getElementById('msg-count');
  if (el) el.textContent = msgCount;
}

function escHtml(str) {
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}

function quickAsk(q) {
  document.getElementById('chat-input').value = q;
  sendMessage();
}

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  addMsg(text, 'user', null);

  const typing = document.getElementById('typing');
  typing.classList.add('show');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId, channel: currentChannel, user_id: 'web_user' })
    });
    const data = await res.json();
    typing.classList.remove('show');
    const tag = data.is_ai_generated ? 'ai' : 'faq';
    addMsg(data.response, 'bot', tag);
  } catch (e) {
    typing.classList.remove('show');
    addMsg('Something went wrong. Please check if the server is running.', 'bot', null);
  }
}

// Enter key to send
document.addEventListener('DOMContentLoaded', () => {
  const inp = document.getElementById('chat-input');
  if (inp) inp.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });
});

// ── Dashboard ──────────────────────────────────────────────────
async function loadDashboard() {
  const el = document.getElementById('dashboard-content');
  el.innerHTML = '<div class="loading"><div class="spin"></div> Loading analytics...</div>';
  try {
    const res = await fetch('/api/admin/analytics');
    const d = await res.json();
    const total = (d.ai_resolved || 0) + (d.faq_resolved || 0);
    const faqPct = total > 0 ? Math.round((d.faq_resolved / total) * 100) : 0;
    const aiPct = total > 0 ? Math.round((d.ai_resolved / total) * 100) : 0;

    el.innerHTML = `
      <div class="kpi-grid">
        <div class="kpi-card blue"><div class="kpi-label">Conversations</div><div class="kpi-val">${d.total_conversations}</div><div class="kpi-sub">All channels</div></div>
        <div class="kpi-card green"><div class="kpi-label">Total Queries</div><div class="kpi-val">${d.total_queries}</div><div class="kpi-sub">User messages</div></div>
        <div class="kpi-card purple"><div class="kpi-label">FAQ Resolved</div><div class="kpi-val">${d.faq_resolved}</div><div class="kpi-sub">${faqPct}% of responses</div></div>
        <div class="kpi-card orange"><div class="kpi-label">AI Resolved</div><div class="kpi-val">${d.ai_resolved}</div><div class="kpi-sub">${aiPct}% of responses</div></div>
      </div>
      <div class="charts-row">
        <div class="chart-card"><h3>Response Type</h3><div class="chart-wrap"><canvas id="typeChart"></canvas></div></div>
        <div class="chart-card"><h3>Channel Split</h3><div class="chart-wrap"><canvas id="chChart"></canvas></div></div>
      </div>
      <div class="top-faq-card">
        <h3>Top Asked Questions</h3>
        ${d.top_faqs && d.top_faqs.length
          ? d.top_faqs.map((f,i) => `<div class="faq-row"><span class="faq-num">${i+1}.</span><span class="faq-text">${escHtml(f.question)}</span><span class="faq-cnt">${f.cnt}×</span></div>`).join('')
          : '<div class="empty"><div class="empty-icon">📭</div><p>No data yet. Start chatting!</p></div>'}
      </div>`;

    setTimeout(() => {
      const tc = document.getElementById('typeChart');
      const cc = document.getElementById('chChart');
      if (tc && window.Chart) {
        new Chart(tc, { type: 'doughnut', data: {
          labels: ['FAQ', 'AI'],
          datasets: [{ data: [d.faq_resolved, d.ai_resolved], backgroundColor: ['#22c55e','#7c3aed'], borderWidth: 0 }]
        }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#94a3b8', font: { size: 11 } } } } } });
      }
      if (cc && window.Chart) {
        const chs = d.channels || {};
        new Chart(cc, { type: 'doughnut', data: {
          labels: Object.keys(chs).map(k => k.charAt(0).toUpperCase() + k.slice(1)),
          datasets: [{ data: Object.values(chs), backgroundColor: ['#4f6ef7','#2ea6d9','#00a884','#0084ff','#e1306c'], borderWidth: 0 }]
        }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#94a3b8', font: { size: 11 } } } } } });
      }
    }, 80);
  } catch(e) {
    el.innerHTML = '<div class="empty"><div class="empty-icon">⚠️</div><p>Failed to load analytics. Is the server running?</p></div>';
  }
}

// ── FAQs ───────────────────────────────────────────────────────
async function loadFAQs(search = '') {
  const url = search ? `/api/admin/faqs?search=${encodeURIComponent(search)}` : '/api/admin/faqs';
  try {
    const res = await fetch(url);
    const data = await res.json();
    allFaqs = data.faqs || [];
    renderFAQs(allFaqs);
  } catch(e) {
    document.getElementById('faq-list').innerHTML = '<div class="empty"><div class="empty-icon">⚠️</div><p>Failed to load FAQs.</p></div>';
  }
}

function renderFAQs(faqs) {
  const el = document.getElementById('faq-list');
  if (!faqs.length) { el.innerHTML = '<div class="empty"><div class="empty-icon">📭</div><p>No FAQs found.</p></div>'; return; }
  el.innerHTML = `<div class="faq-table-wrap"><table>
    <thead><tr><th>Question & Answer</th><th>Category</th><th>Actions</th></tr></thead>
    <tbody>${faqs.map(f => `
      <tr>
        <td><div class="faq-q-text">${escHtml(f.question)}</div><div class="faq-a-text">${escHtml(f.answer.substring(0,110))}${f.answer.length > 110 ? '...' : ''}</div></td>
        <td><span class="cat-badge">${escHtml(f.category || 'General')}</span></td>
        <td><div class="action-btns"><button class="icon-btn edit-btn" onclick="editFAQ(${f.id})">✏️</button><button class="icon-btn del-btn" onclick="deleteFAQ(${f.id})">🗑️</button></div></td>
      </tr>`).join('')}
    </tbody></table></div>`;
}

let searchTimer;
function searchFAQs() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => loadFAQs(document.getElementById('faq-search').value), 300);
}

function openModal() {
  editingFaqId = null;
  document.getElementById('modal-title').textContent = 'Add New FAQ';
  ['faq-cat','faq-q','faq-a','faq-kw'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('faq-cat').value = 'General';
  document.getElementById('modal-overlay').classList.add('show');
}

function editFAQ(id) {
  const faq = allFaqs.find(f => f.id === id);
  if (!faq) return;
  editingFaqId = id;
  document.getElementById('modal-title').textContent = 'Edit FAQ';
  document.getElementById('faq-cat').value = faq.category || 'General';
  document.getElementById('faq-q').value = faq.question;
  document.getElementById('faq-a').value = faq.answer;
  document.getElementById('faq-kw').value = faq.keywords || '';
  document.getElementById('modal-overlay').classList.add('show');
}

function closeModal() { document.getElementById('modal-overlay').classList.remove('show'); }

async function saveFAQ() {
  const body = {
    category: document.getElementById('faq-cat').value.trim() || 'General',
    question: document.getElementById('faq-q').value.trim(),
    answer: document.getElementById('faq-a').value.trim(),
    keywords: document.getElementById('faq-kw').value.trim()
  };
  if (!body.question || !body.answer) { showToast('Question and Answer are required.', 'error'); return; }
  const url = editingFaqId ? `/api/admin/faqs/${editingFaqId}` : '/api/admin/faqs';
  const method = editingFaqId ? 'PUT' : 'POST';
  try {
    const res = await fetch(url, { method, headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) });
    if (!res.ok) throw new Error();
    closeModal();
    loadFAQs();
    showToast(editingFaqId ? 'FAQ updated!' : 'FAQ added!', 'success');
  } catch(e) { showToast('Failed to save.', 'error'); }
}

async function deleteFAQ(id) {
  if (!confirm('Delete this FAQ?')) return;
  try {
    await fetch(`/api/admin/faqs/${id}`, { method: 'DELETE' });
    loadFAQs();
    showToast('FAQ deleted.', 'success');
  } catch(e) { showToast('Failed to delete.', 'error'); }
}

// ── Toast ──────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.className = `toast ${type} show`;
  setTimeout(() => t.className = 'toast', 3000);
}
