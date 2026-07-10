let sessionId = 'web_' + Math.random().toString(36).substr(2,9);
let currentChannel = 'web';
let msgCount = 0;
let editingFaqId = null;
let allFaqs = [];
let recognition = null;
let isListening = false;

const platforms = {
  web: {
    theme: '',
    label: '🌐 Web Chat',
    headerBg: '#1a1d27',
    botName: 'CC Support Bot',
    botSub: '● Online · Always available',
    inputPlaceholder: 'Type your question here...',
    avatarEmoji: '🤖',
    showTimestamps: true,
  },
  telegram: {
    theme: 'theme-telegram',
    label: 'Telegram',
    headerBg: '#1c2733',
    botName: 'CCounselage Bot',
    botSub: 'bot',
    inputPlaceholder: 'Message...',
    avatarEmoji: '🤖',
    showTimestamps: true,
  },
  whatsapp: {
    theme: 'theme-whatsapp',
    label: 'WhatsApp',
    headerBg: '#202c33',
    botName: 'CC Support',
    botSub: 'online',
    inputPlaceholder: 'Message',
    avatarEmoji: '🤖',
    showTimestamps: true,
  },
  messenger: {
    theme: 'theme-messenger',
    label: 'Messenger',
    headerBg: '#16213e',
    botName: 'CloudCounselage',
    botSub: 'Typically replies instantly',
    inputPlaceholder: 'Aa',
    avatarEmoji: '🤖',
    showTimestamps: false,
  },
  instagram: {
    theme: 'theme-instagram',
    label: 'Instagram',
    headerBg: '#121212',
    botName: 'cloudcounselage',
    botSub: 'Active now',
    inputPlaceholder: 'Message...',
    avatarEmoji: '🤖',
    showTimestamps: false,
  },
};

const pageMeta = {
  chat:      { title:'Web Chat',    sub:'AI-powered student support' },
  dashboard: { title:'Dashboard',   sub:'Analytics & performance'    },
  faqs:      { title:'FAQ Manager', sub:'Manage knowledge base'      },
};

document.addEventListener('DOMContentLoaded', () => {
  const sd = document.getElementById('session-display');
  if(sd) sd.textContent = sessionId.substr(0,14)+'...';
  initVoice();
});

// ── Navigation ────────────────────────────────────────────────
function navigate(page) {
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  const pg = document.getElementById('page-'+page);
  if(pg) pg.classList.add('active');
  const nv = document.querySelector(`.nav-item[data-page="${page}"]`);
  if(nv) nv.classList.add('active');
  document.getElementById('page-title').textContent = pageMeta[page].title;
  document.getElementById('page-sub').textContent   = pageMeta[page].sub;
  if(page==='dashboard') loadDashboard();
  if(page==='faqs') loadFAQs();
}

// ── Platform / Theme / UI Switch ──────────────────────────────
function switchChannel(channel, el) {
  currentChannel = channel;
  const p = platforms[channel];

  // Apply body theme class
  document.body.className = p.theme;

  // Active chip
  document.querySelectorAll('.ch-chip').forEach(c=>c.classList.remove('active'));
  el.classList.add('active');

  // Update header
  document.getElementById('platform-label').textContent      = p.label;
  document.getElementById('current-channel-val').textContent = p.label;
  document.getElementById('bot-name').textContent            = p.botName;
  document.getElementById('bot-sub').textContent             = p.botSub;
  document.getElementById('chat-input').placeholder          = p.inputPlaceholder;
  document.getElementById('bot-avatar-emoji').textContent    = p.avatarEmoji;

  // Platform-specific UI tweaks
  applyPlatformUI(channel);

  // Add switch notice in chat
  addMsg(`You are now viewing the ${p.label} interface. Messages sent here are tracked as ${channel} channel.`, 'bot', null);
}

function applyPlatformUI(channel) {
  const header = document.getElementById('chat-header');
  const inputArea = document.getElementById('chat-input-area');
  const sendBtn = document.getElementById('send-btn');

  // Reset
  header.className = 'chat-header';
  sendBtn.textContent = '➤';

  if(channel === 'whatsapp') {
    sendBtn.textContent = '📨';
  } else if(channel === 'telegram') {
    sendBtn.textContent = '➤';
  } else if(channel === 'messenger') {
    sendBtn.textContent = '👍';
  } else if(channel === 'instagram') {
    sendBtn.textContent = '❤️';
  }

  header.classList.add('header-'+channel);
}

// ── Chat ──────────────────────────────────────────────────────
function escHtml(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g,'<br>');
}

function addMsg(text, role, tag) {
  const c = document.getElementById('messages');
  const p = platforms[currentChannel];
  const now = new Date().toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
  const d = document.createElement('div');
  d.className = `msg ${role}`;

  let tagHtml = '';
  if(tag==='faq') tagHtml = `<span class="msg-tag tag-faq">✓ Knowledge base</span>`;
  else if(tag==='ai') tagHtml = `<span class="msg-tag tag-ai">✦ AI generated</span>`;

  d.innerHTML = `
    <div class="msg-bubble">${escHtml(text)}</div>
    <div class="msg-meta">
      ${tagHtml}
      ${p.showTimestamps ? `<span class="msg-time">${now}</span>` : ''}
    </div>`;
  c.appendChild(d);
  c.scrollTop = c.scrollHeight;
  msgCount++;
  const mc=document.getElementById('msg-count');
  if(mc) mc.textContent = msgCount;
}

function quickAsk(q){ document.getElementById('chat-input').value=q; sendMessage(); }

async function sendMessage() {
  const inp = document.getElementById('chat-input');
  const text = inp.value.trim();
  if(!text) return;
  inp.value = '';
  addMsg(text, 'user', null);
  const typing = document.getElementById('typing');
  typing.classList.add('show');
  try {
    const res = await fetch('/api/chat', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({message:text, session_id:sessionId, channel:currentChannel, user_id:'web_user'})
    });
    const data = await res.json();
    typing.classList.remove('show');
    addMsg(data.response, 'bot', data.is_ai_generated ? 'ai' : 'faq');
  } catch(e) {
    typing.classList.remove('show');
    addMsg('Connection error. Please check if the server is running.','bot',null);
  }
}

document.addEventListener('DOMContentLoaded',()=>{
  const inp = document.getElementById('chat-input');
  if(inp) inp.addEventListener('keydown', e=>{
    if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMessage(); }
  });
});

// ── Voice ─────────────────────────────────────────────────────
function initVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const btn = document.getElementById('voice-btn');
  if(!SR){
    if(btn) btn.style.display='none';
    return;
  }
  recognition = new SR();
  recognition.lang = 'en-IN';
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.onresult = e => {
    const transcript = e.results[0][0].transcript;
    document.getElementById('chat-input').value = transcript;
    stopListening();
    sendMessage();
  };
  recognition.onerror = ()=>stopListening();
  recognition.onend   = ()=>stopListening();
}

function toggleVoice() {
  if(!recognition) { initVoice(); }
  if(!recognition) return;
  if(isListening){ stopListening(); return; }
  isListening = true;
  try {
    recognition.start();
    const btn = document.getElementById('voice-btn');
    btn.textContent = '🔴';
    btn.title = 'Listening... click to stop';
    btn.style.background = 'rgba(239,68,68,0.15)';
    btn.style.borderColor = '#ef4444';
    document.getElementById('chat-input').placeholder = '🎤 Listening... speak now';
  } catch(e) { stopListening(); }
}

function stopListening(){
  isListening = false;
  if(recognition) try{ recognition.stop(); }catch(e){}
  const btn = document.getElementById('voice-btn');
  if(btn){
    btn.textContent = '🎤';
    btn.title = 'Click to speak';
    btn.style.background = '';
    btn.style.borderColor = '';
  }
  const inp = document.getElementById('chat-input');
  if(inp) inp.placeholder = platforms[currentChannel].inputPlaceholder;
}

// ── Dashboard ─────────────────────────────────────────────────
async function loadDashboard() {
  const el = document.getElementById('dashboard-content');
  el.innerHTML = '<div class="loading"><div class="spin"></div> Loading...</div>';
  try {
    const res = await fetch('/api/admin/analytics');
    if(!res.ok) throw new Error('HTTP '+res.status);
    const d = await res.json();
    const total = (d.ai_resolved||0)+(d.faq_resolved||0);
    const faqPct = total>0 ? Math.round((d.faq_resolved/total)*100) : 0;
    const aiPct  = total>0 ? Math.round((d.ai_resolved/total)*100)  : 0;
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
        ${d.top_faqs&&d.top_faqs.length
          ? d.top_faqs.map((f,i)=>`<div class="faq-row"><span class="faq-num">${i+1}.</span><span class="faq-text">${escHtml(f.question)}</span><span class="faq-cnt">${f.cnt}×</span></div>`).join('')
          : '<div class="empty"><div class="empty-icon">📭</div><p>No data yet. Start chatting!</p></div>'}
      </div>`;
    setTimeout(()=>{
      const tc=document.getElementById('typeChart');
      const cc=document.getElementById('chChart');
      if(tc&&window.Chart) new Chart(tc,{type:'doughnut',data:{labels:['FAQ','AI'],datasets:[{data:[d.faq_resolved,d.ai_resolved],backgroundColor:['#22c55e','#7c3aed'],borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#94a3b8',font:{size:11}}}}}});
      if(cc&&window.Chart){
        const chs=d.channels||{};
        new Chart(cc,{type:'doughnut',data:{labels:Object.keys(chs).map(k=>k.charAt(0).toUpperCase()+k.slice(1)),datasets:[{data:Object.values(chs),backgroundColor:['#4f6ef7','#2ea6d9','#00a884','#0084ff','#e1306c'],borderWidth:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{labels:{color:'#94a3b8',font:{size:11}}}}}});
      }
    },80);
  } catch(e){
    el.innerHTML = `<div class="empty"><div class="empty-icon">⚠️</div><p>Failed to load analytics: ${e.message}</p></div>`;
  }
}

// ── FAQs ──────────────────────────────────────────────────────
async function loadFAQs(search='') {
  const url = search ? `/api/admin/faqs?search=${encodeURIComponent(search)}` : '/api/admin/faqs';
  const el = document.getElementById('faq-list');
  el.innerHTML = '<div class="loading"><div class="spin"></div> Loading FAQs...</div>';
  try {
    const res = await fetch(url);
    if(!res.ok) throw new Error('HTTP '+res.status);
    const data = await res.json();
    allFaqs = data.faqs||[];
    renderFAQs(allFaqs);
  } catch(e){
    el.innerHTML = `<div class="empty"><div class="empty-icon">⚠️</div><p>Failed: ${e.message}</p></div>`;
  }
}

function renderFAQs(faqs){
  const el = document.getElementById('faq-list');
  if(!faqs.length){ el.innerHTML='<div class="empty"><div class="empty-icon">📭</div><p>No FAQs found.</p></div>'; return; }
  el.innerHTML = `<div class="faq-table-wrap"><table>
    <thead><tr><th>Question & Answer</th><th>Category</th><th>Actions</th></tr></thead>
    <tbody>${faqs.map(f=>`<tr>
      <td><div class="faq-q-text">${escHtml(f.question)}</div><div class="faq-a-text">${escHtml(f.answer.substring(0,120))}${f.answer.length>120?'...':''}</div></td>
      <td><span class="cat-badge">${escHtml(f.category||'General')}</span></td>
      <td><div class="action-btns">
        <button class="icon-btn edit-btn" onclick="editFAQ(${f.id})">✏️</button>
        <button class="icon-btn del-btn" onclick="deleteFAQ(${f.id})">🗑️</button>
      </div></td>
    </tr>`).join('')}</tbody></table></div>`;
}

let searchTimer;
function searchFAQs(){ clearTimeout(searchTimer); searchTimer=setTimeout(()=>loadFAQs(document.getElementById('faq-search').value),300); }

function openModal(){
  editingFaqId=null;
  document.getElementById('modal-title').textContent='Add New FAQ';
  ['faq-cat','faq-q','faq-a','faq-kw'].forEach(id=>document.getElementById(id).value='');
  document.getElementById('faq-cat').value='General';
  document.getElementById('modal-overlay').classList.add('show');
}

function editFAQ(id){
  const faq=allFaqs.find(f=>f.id===id); if(!faq) return;
  editingFaqId=id;
  document.getElementById('modal-title').textContent='Edit FAQ';
  document.getElementById('faq-cat').value=faq.category||'General';
  document.getElementById('faq-q').value=faq.question;
  document.getElementById('faq-a').value=faq.answer;
  document.getElementById('faq-kw').value=faq.keywords||'';
  document.getElementById('modal-overlay').classList.add('show');
}

function closeModal(){ document.getElementById('modal-overlay').classList.remove('show'); }

async function saveFAQ(){
  const body={
    category: document.getElementById('faq-cat').value.trim()||'General',
    question: document.getElementById('faq-q').value.trim(),
    answer:   document.getElementById('faq-a').value.trim(),
    keywords: document.getElementById('faq-kw').value.trim()
  };
  if(!body.question||!body.answer){showToast('Question and Answer required.','error');return;}
  const url=editingFaqId?`/api/admin/faqs/${editingFaqId}`:'/api/admin/faqs';
  const method=editingFaqId?'PUT':'POST';
  try{
    const res=await fetch(url,{method,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    if(!res.ok) throw new Error();
    closeModal(); loadFAQs();
    showToast(editingFaqId?'FAQ updated!':'FAQ added!','success');
  }catch(e){showToast('Failed to save.','error');}
}

async function deleteFAQ(id){
  if(!confirm('Delete this FAQ?')) return;
  try{
    await fetch(`/api/admin/faqs/${id}`,{method:'DELETE'});
    loadFAQs();
    showToast('Deleted.','success');
  }catch(e){showToast('Failed.','error');}
}

function showToast(msg,type='success'){
  const t=document.getElementById('toast');
  t.textContent=msg; t.className=`toast ${type} show`;
  setTimeout(()=>t.className='toast',3000);
}
