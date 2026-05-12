const $ = (sel) => document.querySelector(sel);
const app = $('#app');
const toastEl = $('#toast');

const STR = {
  en: {
    landingTitle: 'Care for the ones who cared for you.',
    landingSub: 'UnityCare brings your whole family together to look after your aging loved one — one shared space for tasks, medications, appointments, and a real AI chat assistant.',
    getStarted: 'Get started free', seeHow: 'See how it works', login: 'Log in', signup: 'Create account', logout: 'Log out',
    features: 'Built for real family care', how: 'How it works', faq: 'FAQ', illustrative: 'Illustrative testimonial',
    email: 'Email address', password: 'Password', fullName: 'Full name', phone: 'Phone number', optional: 'optional', confirmPassword: 'Confirm password',
    remember: 'Remember me', noAccount: "Don't have an account? Create one", haveAccount: 'Already have an account? Log in', terms: 'I agree to the Terms of Service and Privacy Policy',
    incorrect: 'Incorrect email or password. Please try again.', required: 'Please fill the required fields.', create: 'Create account', enter: 'Log in',
    dashboard: 'Dashboard', tasks: 'Tasks', medications: 'Medications', appointments: 'Appointments', family: 'Family', journal: 'Journal', ai: 'AI Assistant', notifications: 'Notifications', settings: 'Settings',
    careRecipient: 'Care recipient profile', addRecipient: 'Add care recipient', editRecipient: 'Edit care recipient', noRecipient: 'No care recipient profile yet',
    noRecipientDesc: 'Create the profile first, then add family members, medications, tasks, appointments, and journal notes manually.',
    recipientName: 'Care recipient full name', recipientNameHelp: 'This is the elderly person or patient your family is caring for.', age: 'Age', relationship: 'Relationship to you', livingSituation: 'Living situation', location: 'City / location', conditions: 'Known health conditions', allergies: 'Allergies', gpName: 'Doctor / GP name', gpPhone: 'Doctor / GP phone',
    openTasks: 'Open tasks', medsCount: 'Medications', membersCount: 'Family members', apptsCount: 'Appointments', addMember: 'Add member', addMedication: 'Add medication', addTask: 'Add task', addAppointment: 'Add appointment', addJournal: 'Add journal entry',
    emptyMembers: 'No family members yet', emptyMeds: 'No medications added', emptyTasks: 'No tasks yet', emptyAppts: 'No appointments scheduled', emptyJournal: 'No journal entries yet',
    memberName: 'Member full name', memberNameHelp: 'The person you want to add to this care group.', memberEmail: 'Member email', memberEmailHelp: 'Used later for invitations and care notifications.', memberPhone: 'Member phone', role: 'Role', roleHelp: 'Primary Carer can manage more. Supporting Carer helps. Remote can stay updated.', notes: 'Notes',
    primary: 'Primary Carer', supporting: 'Supporting Carer', remote: 'Remote / Stays Updated',
    medName: 'Medication name', medNameHelp: 'Example: Lisinopril. Add exactly what is written on the package or prescription.', dosage: 'Dosage', dosageHelp: 'Example: 10mg, 1 tablet, 2 drops.', frequency: 'Frequency', frequencyHelp: 'Example: Morning, Evening, Morning & Evening, As needed.', purpose: 'Purpose / condition', purposeHelp: 'What this medication is for, if known.', doctor: 'Prescribing doctor', refillDate: 'Next refill date',
    taskTitle: 'Task title', taskTitleHelp: 'Short action name, for example: Pick up prescription.', description: 'Description', assignedTo: 'Assigned to', dueDate: 'Due date', status: 'Status', category: 'Category', priority: 'Priority', recurring: 'Recurring',
    apptTitle: 'Appointment title', dateTime: 'Date and time', accompaniedBy: 'Who is taking them?',
    journalText: 'Journal note', journalHelp: 'Write what happened today. The assistant can summarize saved notes using your saved care data.',
    save: 'Save', cancel: 'Cancel', delete: 'Delete', edit: 'Edit', close: 'Close', clear: 'Clear', markAllRead: 'Mark all read',
    aiTitle: 'UnityCare Assistant', aiSub: 'Write your own question. UnityCare AI answers using your saved care data.', aiPlaceholder: 'Type your question here...', aiDisabled: 'Assistant could not answer. Check the server AI settings and try again.',
    aiPrompt1: 'What should I add first?', aiPrompt2: 'Summarise the care group', aiPrompt3: 'What needs attention today?',
    noDataAi: 'Add your care recipient, family members, tasks, medications, or journal entries first so AI has real data to use.',
    authNeeded: 'You must create an account or log in before opening the dashboard.',
    wrongPasswordTest: 'Wrong credentials will stay on this page.',
    careLoad: 'Care load balance', noCareLoad: 'No completed tasks yet. Care load will appear after tasks are added and completed.',
    copied: 'Copied', saved: 'Saved successfully', deleted: 'Deleted', noGoogle: 'Google login was removed because it was not connected to a real provider.',
  },
  ar: {
    landingTitle: 'اعتنِ بمن اعتنى بك.', landingSub: 'يونتي كير يجمع العائلة في مساحة واحدة لرعاية شخص كبير في السن: مهام، أدوية، مواعيد، ومحادثات مهمة.',
    getStarted: 'ابدأ مجاناً', seeHow: 'شاهد الطريقة', login: 'تسجيل الدخول', signup: 'إنشاء حساب', logout: 'تسجيل الخروج',
    features: 'مصمم لرعاية العائلة الحقيقية', how: 'كيف يعمل', faq: 'الأسئلة الشائعة', illustrative: 'رأي توضيحي',
    email: 'البريد الإلكتروني', password: 'كلمة المرور', fullName: 'الاسم الكامل', phone: 'رقم الهاتف', optional: 'اختياري', confirmPassword: 'تأكيد كلمة المرور',
    remember: 'تذكرني', noAccount: 'لا تملك حساباً؟ أنشئ حساباً', haveAccount: 'لديك حساب؟ سجل الدخول', terms: 'أوافق على الشروط وسياسة الخصوصية',
    incorrect: 'البريد الإلكتروني أو كلمة المرور غير صحيحة.', required: 'يرجى تعبئة الحقول المطلوبة.', create: 'إنشاء الحساب', enter: 'تسجيل الدخول',
    dashboard: 'لوحة التحكم', tasks: 'المهام', medications: 'الأدوية', appointments: 'المواعيد', family: 'العائلة', journal: 'السجل', ai: 'المساعد الذكي', notifications: 'الإشعارات', settings: 'الإعدادات',
    careRecipient: 'ملف متلقي الرعاية', addRecipient: 'إضافة متلقي الرعاية', editRecipient: 'تعديل متلقي الرعاية', noRecipient: 'لا يوجد ملف متلقي رعاية بعد',
    noRecipientDesc: 'أنشئ الملف أولاً، ثم أضف العائلة والأدوية والمهام والمواعيد والملاحظات يدوياً.',
    recipientName: 'الاسم الكامل لمتلقي الرعاية', recipientNameHelp: 'الشخص الكبير في السن أو المريض الذي ترعاه العائلة.', age: 'العمر', relationship: 'صلة القرابة', livingSituation: 'حالة السكن', location: 'المدينة / الموقع', conditions: 'الحالات الصحية المعروفة', allergies: 'الحساسية', gpName: 'اسم الطبيب', gpPhone: 'رقم الطبيب',
    openTasks: 'مهام مفتوحة', medsCount: 'الأدوية', membersCount: 'أفراد العائلة', apptsCount: 'المواعيد', addMember: 'إضافة عضو', addMedication: 'إضافة دواء', addTask: 'إضافة مهمة', addAppointment: 'إضافة موعد', addJournal: 'إضافة ملاحظة',
    emptyMembers: 'لا يوجد أفراد عائلة بعد', emptyMeds: 'لا توجد أدوية', emptyTasks: 'لا توجد مهام', emptyAppts: 'لا توجد مواعيد', emptyJournal: 'لا توجد ملاحظات',
    memberName: 'اسم العضو الكامل', memberNameHelp: 'الشخص الذي تريد إضافته إلى مجموعة الرعاية.', memberEmail: 'بريد العضو', memberEmailHelp: 'يستخدم لاحقاً للدعوات والإشعارات.', memberPhone: 'هاتف العضو', role: 'الدور', roleHelp: 'المسؤول الأساسي يدير أكثر، المساعد يشارك، والمتابع يرى التحديثات.', notes: 'ملاحظات',
    primary: 'المسؤول الأساسي', supporting: 'مساعد رعاية', remote: 'متابع عن بُعد',
    medName: 'اسم الدواء', medNameHelp: 'مثال: Lisinopril. اكتب الاسم كما هو على الوصفة.', dosage: 'الجرعة', dosageHelp: 'مثال: 10mg أو قرص واحد.', frequency: 'التكرار', frequencyHelp: 'مثال: صباحاً، مساءً، عند الحاجة.', purpose: 'الغرض / الحالة', purposeHelp: 'لماذا يستخدم الدواء إن كان معروفاً.', doctor: 'الطبيب الواصف', refillDate: 'تاريخ إعادة التعبئة',
    taskTitle: 'عنوان المهمة', taskTitleHelp: 'اسم قصير مثل: استلام الدواء.', description: 'الوصف', assignedTo: 'مكلف إلى', dueDate: 'تاريخ الاستحقاق', status: 'الحالة', category: 'التصنيف', priority: 'الأولوية', recurring: 'التكرار',
    apptTitle: 'عنوان الموعد', dateTime: 'التاريخ والوقت', accompaniedBy: 'من سيأخذه؟', journalText: 'ملاحظة السجل', journalHelp: 'اكتب ما حدث اليوم.',
    save: 'حفظ', cancel: 'إلغاء', delete: 'حذف', edit: 'تعديل', close: 'إغلاق', clear: 'مسح', markAllRead: 'تحديد الكل كمقروء',
    aiTitle: 'مساعد UnityCare', aiSub: 'اكتب سؤالك بنفسك. يجيب مساعد UnityCare باستخدام بيانات الرعاية المحفوظة.', aiPlaceholder: 'اكتب سؤالك هنا...', aiDisabled: 'تعذر على المساعد الإجابة. تحقق من إعدادات الذكاء على الخادم وحاول مرة أخرى.',
    aiPrompt1: 'ماذا أضيف أولاً؟', aiPrompt2: 'لخص مجموعة الرعاية', aiPrompt3: 'ما الذي يحتاج انتباه اليوم؟',
    noDataAi: 'أضف البيانات أولاً حتى يستخدمها الذكاء.', authNeeded: 'يجب إنشاء حساب أو تسجيل الدخول قبل فتح لوحة التحكم.', wrongPasswordTest: 'البيانات الخاطئة ستبقيك في هذه الصفحة.',
    careLoad: 'توازن الرعاية', noCareLoad: 'سيظهر التوازن بعد إضافة وإنجاز المهام.', copied: 'تم النسخ', saved: 'تم الحفظ', deleted: 'تم الحذف', noGoogle: 'تم حذف تسجيل الدخول بجوجل لأنه غير مربوط بمزود حقيقي.',
  }
};

const state = {
  booted: false,
  user: null,
  data: null,
  route: 'landing',
  lang: 'en',
  sidebarCollapsed: localStorage.getItem('uc_sidebar') === '1',
  aiHidden: localStorage.getItem('uc_ai_hidden') === '1',
  modal: null,
  editItem: null,
  aiMessages: [],
  aiBusy: false,
  error: '',
};

const internalRoutes = new Set(['dashboard','tasks','medications','appointments','family','journal','ai','notifications','settings','onboarding']);
const navItems = [
  ['dashboard','⌂'], ['tasks','☑'], ['medications','◈'], ['appointments','◷'], ['family','◉'], ['journal','☰'], ['ai','✦'], ['notifications','●'], ['settings','⚙']
];

function t(key){ return (STR[state.lang] && STR[state.lang][key]) || STR.en[key] || key; }
function esc(v){ return String(v ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
function initials(name){ return (name||'?').split(/\s+/).filter(Boolean).map(x=>x[0]).join('').slice(0,2).toUpperCase(); }
function go(route){ location.hash = route; }
function routeFromHash(){ return (location.hash.replace('#','') || 'landing').split('?')[0]; }
function setLang(lang){ state.lang=lang; document.documentElement.lang=lang; document.documentElement.dir=lang==='ar'?'rtl':'ltr'; document.body.classList.toggle('rtl', lang==='ar'); render(); }
function showToast(msg){ toastEl.textContent = msg; toastEl.hidden=false; setTimeout(()=>toastEl.hidden=true, 2600); }

async function api(path, opts={}){
  const res = await fetch(path, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(opts.headers||{}) },
    ...opts,
    body: opts.body && typeof opts.body !== 'string' ? JSON.stringify(opts.body) : opts.body
  });
  const data = await res.json().catch(()=>({ok:false,error:'Invalid server response'}));
  if(!res.ok || data.ok === false){
    const err = new Error(data.error || 'Request failed');
    err.status = res.status; err.data = data;
    throw err;
  }
  return data;
}

async function boot(){
  state.route = routeFromHash();
  try{
    const me = await api('/api/auth/me');
    state.user = me.user;
    if(me.user) state.lang = me.user.language || 'en';
  }catch(e){ state.user = null; }
  setLang(state.lang);
  await ensureRoute();
  state.booted = true;
  setTimeout(()=>$('#splash')?.classList.add('hide'), 700);
}

async function ensureRoute(){
  state.route = routeFromHash();
  if(internalRoutes.has(state.route) && !state.user){
    state.error = t('authNeeded');
    state.route = 'login';
    location.hash = 'login';
  }
  if(state.user && ['landing','login','signup'].includes(state.route)){
    state.route = state.user.onboardingComplete ? 'dashboard' : 'onboarding';
    location.hash = state.route;
  }
  if(state.user){
    await loadData();
    if(state.route === 'ai') await loadAiMessages();
  }
  render();
}

async function loadData(){
  try{
    const res = await api('/api/dashboard');
    state.data = res.data;
  }catch(e){
    if(e.status === 401){ state.user=null; go('login'); }
  }
}
async function loadAiMessages(){
  try{ state.aiMessages = (await api('/api/ai/messages')).messages || []; }catch(e){ state.aiMessages=[]; }
}

function logo(compact=false){ return `<div class="logo ${compact?'compact':''}"><img src="/assets/unitycare-logo.svg" alt="UnityCare logo"></div>`; }
function publicNav(){ return `<div class="nav-public glass">${logo()}<div class="row"><div class="lang-toggle"><button class="${state.lang==='en'?'active':''}" onclick="setLang('en')">EN</button><button class="${state.lang==='ar'?'active':''}" onclick="setLang('ar')">ع</button></div><button class="btn ghost" onclick="go('login')">${t('login')}</button><button class="btn primary" onclick="go('signup')">${t('signup')}</button></div></div>`; }

function landing(){
  return `<div class="page landing">
    ${publicNav()}
    <section class="hero">
      <div>
        <span class="eyebrow">UnityCare • AI family care coordinator</span>
        <h1 class="title">${t('landingTitle')}</h1>
        <p class="subtitle">${t('landingSub')}</p>
        <div class="hero-actions"><button class="btn primary" onclick="go('signup')">${t('getStarted')}</button><a class="btn" href="#features">${t('seeHow')}</a></div>
      </div>
      <div class="illustration glass">
        <div class="family-orbit"><div class="heart-big">♡</div><div class="person p1">UC</div><div class="person p2">👩</div><div class="person p3">👨</div></div>
      </div>
    </section>
    <section id="features" class="section glass"><h2>${t('how')}</h2><p class="muted">Create the care profile, invite your family, then coordinate care with real saved data and real login protection.</p><div class="grid cols-3">
      ${feature('①','Create profile','Add the care recipient manually. No fake parent or demo data is created.')}
      ${feature('②','Invite or add family','Add members manually with clear fields for name, email, phone, role, and notes.')}
      ${feature('③','Coordinate together','Tasks, medication, appointments, journal, notifications, and AI all use saved SQLite data.')}
    </div></section>
    <section class="section glass"><h2>${t('features')}</h2><div class="grid cols-3">
      ${feature('☑','Shared task board','Assign and track care responsibilities with To Do, In Progress, and Done states.')}
      ${feature('◈','Medication tracker','Add medication name, dosage, frequency, purpose, doctor, refill date, and notes.')}
      ${feature('✦','AI care assistant','Type your own care questions. The assistant answers through OpenRouter using the real SQLite data you add.')}
      ${feature('☰','Care journal','Write daily notes and keep them attached to your real account and group.')}
      ${feature('◉','Family coordination','See manually added members, their roles, and care load.')}
      ${feature('⚑','No bypass login','Dashboard APIs require a valid session. Wrong credentials do not enter the app.')}
    </div></section>
    <section class="section glass"><h2>${t('faq')}</h2><div class="grid cols-2">
      ${feature('Q','Is there Google login?','No. It was removed because it was not connected to a real provider.')}
      ${feature('Q','Can I enter without an account?','No. Internal API routes require a valid httpOnly session cookie.')}
      ${feature('Q','Does data persist?','Yes. All data is saved in the SQLite database in the data folder.')}
      ${feature('Q','How does the assistant answer?','The assistant uses the configured AI provider and the saved SQLite data from your UnityCare account.')}
    </div></section>
    <footer class="footer-public glass">${logo()}<span class="muted">© UnityCare</span></footer>
  </div>`;
}
function feature(icon,title,body){ return `<article class="feature-card"><div class="feature-icon">${icon}</div><h3>${esc(title)}</h3><p>${esc(body)}</p></article>`; }

function authPage(mode='login'){
  const isSignup = mode==='signup';
  return `<div class="page auth-wrap"><div class="auth-card glass">
    <aside class="auth-brand">${logo()}<h1 class="title">${isSignup?t('signup'):t('login')}</h1><p class="subtitle">${isSignup?'Create a real account first. The dashboard is locked until sign-up or valid login.':t('wrongPasswordTest')}</p><div class="success">${t('noGoogle')}</div></aside>
    <section class="auth-form">
      <div class="row" style="justify-content:space-between;margin-bottom:16px"><button class="btn ghost" onclick="go('landing')">← UnityCare</button><div class="lang-toggle"><button class="${state.lang==='en'?'active':''}" onclick="setLang('en')">EN</button><button class="${state.lang==='ar'?'active':''}" onclick="setLang('ar')">ع</button></div></div>
      <div class="tabs"><button class="btn ${!isSignup?'active':''}" onclick="go('login')">${t('login')}</button><button class="btn ${isSignup?'active':''}" onclick="go('signup')">${t('signup')}</button></div>
      <form onsubmit="submitAuth(event,'${mode}')">
        ${isSignup ? field('fullName',t('fullName'),'text','',true,'Your real account display name.') : ''}
        ${field('email',t('email'),'email','',true,'')}
        ${isSignup ? field('phone',`${t('phone')} (${t('optional')})`,'tel','',false,'') : ''}
        ${field('password',t('password'),'password','',true,isSignup?'Minimum 8 characters. Stored hashed in the database.':'')}
        ${isSignup ? `<div class="strength"><i id="strengthBar"></i></div>${field('confirmPassword',t('confirmPassword'),'password','',true,'')}
        <label class="field"><span>Language</span><div class="lang-toggle"><button type="button" class="${state.lang==='en'?'active':''}" onclick="setLang('en')">English 🇬🇧</button><button type="button" class="${state.lang==='ar'?'active':''}" onclick="setLang('ar')">العربية 🇸🇦</button></div></label>
        <label class="field"><div class="input-wrap"><input id="terms" type="checkbox" style="width:auto" required><span style="margin:0">${t('terms')}</span></div></label>` : `<label class="field"><div class="input-wrap"><input id="remember" type="checkbox" style="width:auto"><span style="margin:0">${t('remember')}</span></div></label>`}
        <div id="authError"></div>
        <button class="btn primary" style="width:100%;margin-top:6px" type="submit">${isSignup?t('create'):t('enter')}</button>
        <button class="btn ghost" style="width:100%;margin-top:10px" type="button" onclick="go('${isSignup?'login':'signup'}')">${isSignup?t('haveAccount'):t('noAccount')}</button>
      </form>
    </section>
  </div></div>`;
}
function field(id,label,type='text',value='',required=false,help=''){
  return `<label class="field"><span>${esc(label)}${required?' *':''}</span><div class="input-wrap"><input id="${id}" name="${id}" type="${type}" value="${esc(value)}" ${required?'required':''}></div>${help?`<small>${esc(help)}</small>`:''}</label>`;
}
window.submitAuth = async function(ev,mode){
  ev.preventDefault(); const fd = new FormData(ev.target); const errEl = $('#authError'); errEl.innerHTML='';
  try{
    if(mode==='signup'){
      const pass = fd.get('password');
      if(pass !== fd.get('confirmPassword')) throw new Error('Passwords do not match.');
      const res = await api('/api/auth/signup',{method:'POST',body:{fullName:fd.get('fullName'),email:fd.get('email'),phone:fd.get('phone'),password:pass,language:state.lang}});
      state.user = res.user; state.lang = res.user.language || state.lang; showToast('Welcome to UnityCare'); go('onboarding');
    }else{
      const res = await api('/api/auth/login',{method:'POST',body:{email:fd.get('email'),password:fd.get('password'),remember:$('#remember')?.checked}});
      state.user = res.user; state.lang = res.user.language || state.lang; showToast('Logged in'); go(res.user.onboardingComplete?'dashboard':'onboarding');
    }
  }catch(e){
    let msg = e.message || t('incorrect');
    if(e.data?.lockoutSeconds) msg += ` (${Math.ceil(e.data.lockoutSeconds/60)} min)`;
    errEl.innerHTML = `<div class="error">${esc(msg)}</div>`;
  }
};
document.addEventListener('input', e=>{
  if(e.target.id==='password'){
    const p=e.target.value; let s=0; if(p.length>=8)s++; if(/[A-Z]/.test(p))s++; if(/[0-9]/.test(p))s++; if(/[^A-Za-z0-9]/.test(p))s++;
    const bar=$('#strengthBar'); if(bar) bar.style.width=(s*25)+'%';
  }
});

function shell(inner){
  const d = state.data || {counts:{}, careRecipient:null, familyMembers:[], medications:[], tasks:[], appointments:[], journalEntries:[], notifications:[]};
  return `<div class="page app-shell">
    <aside class="sidebar glass ${state.sidebarCollapsed?'collapsed':''}">
      <div class="sidebar-top">${logo(state.sidebarCollapsed)}<button class="icon-btn" onclick="toggleSidebar()" title="Minimize sidebar">${state.sidebarCollapsed?'→':'←'}</button></div>
      <nav class="side-nav">${navItems.map(([r,ico])=>`<button class="side-link ${state.route===r?'active':''}" onclick="go('${r}')"><span class="ico">${ico}</span><span class="hide-collapsed">${t(r)}</span></button>`).join('')}</nav>
      <div class="recipient-mini hide-collapsed"><b>${t('careRecipient')}</b><p class="muted">${d.careRecipient?esc(d.careRecipient.recipient_name):t('noRecipient')}</p></div>
    </aside>
    <main class="main">
      <header class="topbar glass"><h1>${t(state.route)}</h1><div class="search input-wrap"><input placeholder="Search tasks, medications, journal..." oninput="globalSearch(this.value)"></div><button class="icon-btn" onclick="toggleAi()" title="Show/hide AI">✦</button><button class="icon-btn" onclick="go('notifications')" title="Notifications">●</button><div class="avatar">${initials(state.user?.fullName)}</div><button class="btn small" onclick="logout()">${t('logout')}</button></header>
      ${inner}
    </main>
    <nav class="mobile-nav glass">${navItems.slice(0,5).map(([r,ico])=>`<button class="${state.route===r?'active':''}" onclick="go('${r}')"><div>${ico}</div>${t(r)}</button>`).join('')}</nav>
  </div>`;
}
window.toggleSidebar=()=>{state.sidebarCollapsed=!state.sidebarCollapsed; localStorage.setItem('uc_sidebar',state.sidebarCollapsed?'1':'0'); render();};
window.toggleAi=()=>{state.aiHidden=!state.aiHidden; localStorage.setItem('uc_ai_hidden',state.aiHidden?'1':'0'); render();};
window.logout=async()=>{await api('/api/auth/logout',{method:'POST',body:{}}).catch(()=>{}); state.user=null; state.data=null; go('landing');};

function dashboard(){
  const d=state.data; const c=d.counts||{};
  return shell(`<div class="content-grid"><section class="stack">
    ${recipientCard()}
    <div class="stats">${stat(t('openTasks'),c.openTasks||0,'☑')}${stat(t('medsCount'),c.medications||0,'◈')}${stat(t('membersCount'),c.familyMembers||0,'◉')}${stat(t('apptsCount'),c.appointments||0,'◷')}</div>
    <div class="grid cols-2"><div class="card glass">${quickList('tasks',t('tasks'),d.tasks,t('emptyTasks'))}</div><div class="card glass">${quickList('medications',t('medications'),d.medications,t('emptyMeds'))}</div></div>
    <div class="grid cols-2"><div class="card glass">${quickList('appointments',t('appointments'),d.appointments,t('emptyAppts'))}</div><div class="card glass">${careLoad()}</div></div>
  </section>${state.aiHidden?'':aiPanel(false)}</div>`);
}
function stat(label,value,ico){return `<div class="stat"><div>${ico}</div><strong>${esc(value)}</strong><span class="muted">${esc(label)}</span></div>`;}
function recipientCard(){
  const p=state.data?.careRecipient;
  if(!p) return `<div class="card glass empty"><div class="empty-icon">♡</div><h2>${t('noRecipient')}</h2><p>${t('noRecipientDesc')}</p><button class="btn primary" onclick="openModal('recipient')">${t('addRecipient')}</button></div>`;
  return `<div class="recipient-card card glass"><div class="recipient-avatar">${initials(p.recipient_name)}</div><div><div class="muted">${t('careRecipient')}</div><h2 class="recipient-name">${esc(p.recipient_name)}</h2><div class="row" style="margin-top:12px"><span class="pill">${t('age')}: ${esc(p.recipient_age||'—')}</span><span class="pill">${esc(p.relationship||'Care recipient')}</span><span class="pill">${esc(p.location||'No location')}</span></div></div><button class="btn" onclick="openModal('recipient')">${t('edit')}</button></div>`;
}
function quickList(type,title,items,emptyMsg){
  const btn = {tasks:'addTask', medications:'addMedication', appointments:'addAppointment'}[type];
  const modal = {tasks:'task', medications:'medication', appointments:'appointment'}[type];
  return `<div class="page-head"><h2>${title}</h2>${btn?`<button class="btn primary small" onclick="openModal('${modal}')">${t(btn)}</button>`:''}</div>` +
    (items?.length ? `<div class="list">${items.slice(0,3).map(itemCard).join('')}</div>` : empty(emptyMsg, btn? t(btn):'', modal));
}
function empty(msg,btn='',modal=''){ return `<div class="empty"><div class="empty-icon">＋</div><p>${esc(msg)}</p>${btn?`<button class="btn primary" onclick="openModal('${modal}')">${esc(btn)}</button>`:''}</div>`; }

function itemCard(x){
  if(x.recipient_name) return '';
  const title = x.title || x.name || x.entry_text || x.message || 'Item';
  let kv='';
  if(x.email) kv += `<b>Email</b><span>${esc(x.email)}</span><b>${t('role')}</b><span>${esc(roleLabel(x.role))}</span>`;
  if(x.dosage || x.frequency || x.purpose) kv += `<b>${t('dosage')}</b><span>${esc(x.dosage||'—')}</span><b>${t('frequency')}</b><span>${esc(x.frequency||'—')}</span><b>${t('purpose')}</b><span>${esc(x.purpose||'—')}</span>`;
  if(x.due_date || x.status || x.assigned_name) kv += `<b>${t('status')}</b><span>${esc(x.status||'todo')}</span><b>${t('assignedTo')}</b><span>${esc(x.assigned_name||'Unassigned')}</span><b>${t('dueDate')}</b><span>${esc(x.due_date||'No due date')}</span>`;
  if(x.appointment_datetime || x.doctor_name) kv += `<b>${t('dateTime')}</b><span>${esc(x.appointment_datetime||'—')}</span><b>${t('doctor')}</b><span>${esc(x.doctor_name||'—')}</span><b>${t('accompaniedBy')}</b><span>${esc(x.accompanied_by_name||'Unassigned')}</span>`;
  if(x.entry_text) kv += `<b>Author</b><span>${esc(x.author_name||state.user?.fullName)}</span><b>Created</b><span>${esc(x.created_at||'')}</span>`;
  return `<article class="item"><div class="item-head"><div class="item-title">${esc(title)}</div>${x.priority?`<span class="pill">${esc(x.priority)}</span>`:''}</div>${kv?`<div class="kv">${kv}</div>`:''}</article>`;
}
function roleLabel(role){ return role==='primary'?t('primary'):role==='supporting'?t('supporting'):role==='remote'?t('remote'):role; }

function familyPage(){ const m=state.data.familyMembers||[]; return shell(`<div class="content-grid"><section class="stack"><div class="card glass"><div class="page-head"><div><h2>${t('family')}</h2><p class="muted">Add every member manually. Nothing is pre-filled.</p></div><button class="btn primary" onclick="openModal('member')">${t('addMember')}</button></div>${m.length?`<div class="grid cols-3">${m.map(memberCard).join('')}</div>`:empty(t('emptyMembers'),t('addMember'),'member')}</div><div class="card glass">${careLoad()}</div></section>${state.aiHidden?'':aiPanel(false)}</div>`); }
function memberCard(m){ return `<article class="item"><div class="item-head"><div class="row"><div class="avatar">${initials(m.name)}</div><div><div class="item-title">${esc(m.name)}</div><div class="muted">${esc(m.email)}</div></div></div><span class="pill">${roleLabel(m.role)}</span></div><div class="kv"><b>${t('memberPhone')}</b><span>${esc(m.phone||'—')}</span><b>${t('role')}</b><span>${roleLabel(m.role)}</span><b>${t('notes')}</b><span>${esc(m.notes||'—')}</span></div><div class="row" style="margin-top:14px"><button class="btn small" onclick="editEntity('member',${m.id})">${t('edit')}</button><button class="btn danger small" onclick="deleteEntity('members',${m.id})">${t('delete')}</button></div></article>`; }

function medicationsPage(){ const meds=state.data.medications||[]; return shell(`<div class="content-grid"><section class="card glass"><div class="page-head"><div><h2>${t('medications')}</h2><p class="muted">Every field is labelled so you know exactly what variable you are adding.</p></div><button class="btn primary" onclick="openModal('medication')">${t('addMedication')}</button></div>${meds.length?`<div class="grid cols-2">${meds.map(medCard).join('')}</div>`:empty(t('emptyMeds'),t('addMedication'),'medication')}</section>${state.aiHidden?'':aiPanel(false)}</div>`); }
function medCard(m){ return `<article class="item"><div class="item-head"><div class="item-title">${esc(m.name)}</div><span class="pill">${esc(m.frequency||'No frequency')}</span></div><div class="kv"><b>${t('dosage')}</b><span>${esc(m.dosage||'—')}</span><b>${t('purpose')}</b><span>${esc(m.purpose||'—')}</span><b>${t('doctor')}</b><span>${esc(m.prescribing_doctor||'—')}</span><b>${t('refillDate')}</b><span>${esc(m.refill_date||'—')}</span><b>${t('notes')}</b><span>${esc(m.notes||'—')}</span></div><div class="row" style="margin-top:14px"><button class="btn small" onclick="editEntity('medication',${m.id})">${t('edit')}</button><button class="btn danger small" onclick="deleteEntity('medications',${m.id})">${t('delete')}</button></div></article>`; }

function tasksPage(){ const tasks=state.data.tasks||[]; const groups={todo:[],progress:[],done:[]}; tasks.forEach(x=>groups[x.status||'todo']?.push(x)); return shell(`<div class="content-grid"><section class="card glass"><div class="page-head"><div><h2>${t('tasks')}</h2><p class="muted">Add tasks manually; assign them to members you added.</p></div><button class="btn primary" onclick="openModal('task')">${t('addTask')}</button></div>${tasks.length?`<div class="kanban">${['todo','progress','done'].map(k=>`<div class="column"><h3>${k==='todo'?'To Do':k==='progress'?'In Progress':'Done'} <span class="pill">${groups[k].length}</span></h3><div class="list">${groups[k].map(taskCard).join('')||'<p class="muted">Empty</p>'}</div></div>`).join('')}</div>`:empty(t('emptyTasks'),t('addTask'),'task')}</section>${state.aiHidden?'':aiPanel(false)}</div>`); }
function taskCard(x){ return `<article class="item"><div class="item-title">${esc(x.title)}</div><div class="kv"><b>${t('assignedTo')}</b><span>${esc(x.assigned_name||'Unassigned')}</span><b>${t('dueDate')}</b><span>${esc(x.due_date||'—')}</span><b>${t('category')}</b><span>${esc(x.category||'—')}</span><b>${t('priority')}</b><span>${esc(x.priority||'normal')}</span></div><div class="row" style="margin-top:14px"><button class="btn small" onclick="editEntity('task',${x.id})">${t('edit')}</button><button class="btn danger small" onclick="deleteEntity('tasks',${x.id})">${t('delete')}</button></div></article>`; }

function appointmentsPage(){ const a=state.data.appointments||[]; return shell(`<div class="content-grid"><section class="card glass"><div class="page-head"><div><h2>${t('appointments')}</h2><p class="muted">Appointments are saved with date/time, doctor, location, and who is taking the care recipient.</p></div><button class="btn primary" onclick="openModal('appointment')">${t('addAppointment')}</button></div>${a.length?`<div class="list">${a.map(apptCard).join('')}</div>`:empty(t('emptyAppts'),t('addAppointment'),'appointment')}</section>${state.aiHidden?'':aiPanel(false)}</div>`); }
function apptCard(x){ return `<article class="item"><div class="item-title">${esc(x.title)}</div><div class="kv"><b>${t('dateTime')}</b><span>${esc(x.appointment_datetime||'—')}</span><b>${t('doctor')}</b><span>${esc(x.doctor_name||'—')}</span><b>${t('location')}</b><span>${esc(x.location||'—')}</span><b>${t('accompaniedBy')}</b><span>${esc(x.accompanied_by_name||'Unassigned')}</span><b>${t('notes')}</b><span>${esc(x.notes||'—')}</span></div><div class="row" style="margin-top:14px"><button class="btn small" onclick="editEntity('appointment',${x.id})">${t('edit')}</button><button class="btn danger small" onclick="deleteEntity('appointments',${x.id})">${t('delete')}</button></div></article>`; }

function journalPage(){ const j=state.data.journalEntries||[]; return shell(`<div class="content-grid"><section class="card glass"><div class="page-head"><div><h2>${t('journal')}</h2><p class="muted">Keep real observations. Nothing is generated here.</p></div><button class="btn primary" onclick="openModal('journal')">${t('addJournal')}</button></div>${j.length?`<div class="list">${j.map(entry=>`<article class="item"><div class="item-head"><div class="item-title">${esc(entry.author_name||state.user.fullName)}</div><span class="pill">${esc(entry.created_at)}</span></div><p>${esc(entry.entry_text)}</p><button class="btn danger small" onclick="deleteEntity('journal',${entry.id})">${t('delete')}</button></article>`).join('')}</div>`:empty(t('emptyJournal'),t('addJournal'),'journal')}</section>${state.aiHidden?'':aiPanel(false)}</div>`); }

function notificationsPage(){ const n=state.data.notifications||[]; return shell(`<section class="card glass"><div class="page-head"><div><h2>${t('notifications')}</h2><p class="muted">Notifications are from your real saved app data.</p></div><button class="btn" onclick="markAllRead()">${t('markAllRead')}</button></div>${n.length?`<div class="list">${n.map(x=>`<article class="item"><div class="item-head"><div class="item-title">${esc(x.message)}</div><span class="pill">${x.read?'Read':'Unread'}</span></div><div class="muted">${esc(x.type)} · ${esc(x.created_at)}</div></article>`).join('')}</div>`:empty('You are all caught up')}</section>`); }
window.markAllRead=async()=>{await api('/api/notifications/read-all',{method:'POST',body:{}}); await loadData(); render();};

function settingsPage(){ return shell(`<section class="card glass"><h2>${t('settings')}</h2><div class="grid cols-2"><div class="item"><h3>Profile</h3><div class="kv"><b>${t('fullName')}</b><span>${esc(state.user.fullName)}</span><b>${t('email')}</b><span>${esc(state.user.email)}</span><b>${t('phone')}</b><span>${esc(state.user.phone||'—')}</span></div></div><div class="item"><h3>Language</h3><div class="lang-toggle"><button class="${state.lang==='en'?'active':''}" onclick="setLang('en')">English</button><button class="${state.lang==='ar'?'active':''}" onclick="setLang('ar')">العربية</button></div><p class="muted">This changes the UI direction immediately. Server language is saved at signup in this v4 build.</p></div><div class="item danger-zone"><h3>Security check</h3><p>No dashboard page can read/write data unless the server confirms your session cookie. Wrong login credentials stay on login.</p></div></div></section>`); }

function onboardingPage(){ return shell(`<section class="card glass"><h2>${t('careRecipient')}</h2><p class="muted">Step 1: add the care recipient manually. The app does not create a fake parent or member for you.</p><form onsubmit="saveRecipientFromPage(event)">${recipientFormHtml()}<div id="pageError"></div><button class="btn primary" type="submit">${t('save')}</button></form></section>`); }
window.saveRecipientFromPage=async(ev)=>{ev.preventDefault(); const obj=Object.fromEntries(new FormData(ev.target).entries()); try{await saveRecipient(obj);}catch(e){$('#pageError').innerHTML=`<div class="error">${esc(e.message)}</div>`;}};

function careLoad(){
  const members = state.data.familyMembers||[]; const tasks = state.data.tasks||[]; const done = tasks.filter(x=>x.status==='done' && x.assigned_to_member_id);
  if(!members.length || !done.length) return `<h2>${t('careLoad')}</h2><div class="empty"><p>${t('noCareLoad')}</p></div>`;
  return `<h2>${t('careLoad')}</h2><div class="bars">${members.map(m=>{const count=done.filter(x=>x.assigned_to_member_id===m.id).length; const pct=Math.round(count/done.length*100)||0; return `<div class="bar-line"><b>${esc(m.name)}</b><div class="bar"><i style="width:${pct}%"></i></div><span>${pct}%</span></div>`}).join('')}</div>`;
}

function aiPanel(full=false){
  const messages = full ? state.aiMessages : state.aiMessages.slice(-6);
  const inputId = full ? 'aiMessageFull' : 'aiMessageSide';
  const placeholder = t('aiPlaceholder');
  return `<aside class="ai-panel card glass ${full?'full-ai':''}"><div class="ai-head"><div class="spark">✦</div><div><h2 style="margin:0">${t('aiTitle')}</h2><div class="muted">${t('aiSub')}</div></div></div>
    <div id="chatBox" class="chat-box">${messages.length?messages.map(m=>`<div class="bubble ${m.role==='user'?'user':'assistant'} ${m.error?'error-bubble':''}">${esc(m.content)}</div>`).join(''):`<div class="empty"><div class="empty-icon">✦</div><p>${t('noDataAi')}</p></div>`}${state.aiBusy?`<div class="bubble assistant"><span class="typing"><i></i><i></i><i></i></span></div>`:''}</div>
    <form class="ai-compose" onsubmit="submitAi(event, '${inputId}')">
      <textarea id="${inputId}" rows="${full?3:2}" placeholder="${esc(placeholder)}" ${state.aiBusy?'disabled':''}></textarea>
      <button class="btn primary" type="submit" ${state.aiBusy?'disabled':''}>${state.lang==='ar'?'إرسال':'Send'}</button>
    </form>
    <div class="ai-hint">${state.lang==='ar'?'اكتب سؤالاً عن المهام، الأدوية، المواعيد، أفراد العائلة، السجل، أو بطاقة الطوارئ.':'Ask about tasks, medications, appointments, family members, journal notes, or emergency information.'}</div>
  </aside>`;
}
function aiPage(){ return shell(aiPanel(true)); }
window.submitAi=async(ev,inputId)=>{
  ev.preventDefault();
  const input = document.getElementById(inputId);
  const message = (input?.value || '').trim();
  if(!message) return;
  if(input) input.value = '';
  await sendAi(message);
};
window.sendAi=async(text)=>{
  const message = String(text || '').trim();
  if(!message || state.aiBusy) return;
  state.aiMessages.push({role:'user',content:message,created_at:new Date().toISOString()});
  state.aiBusy=true;
  render();
  setTimeout(()=>{const box=$('#chatBox'); if(box) box.scrollTop=box.scrollHeight;},20);
  try{
    const res=await api('/api/ai/chat',{method:'POST',body:{message}});
    if(res.reply){
      state.aiMessages.push({role:'assistant',content:res.reply,created_at:res.createdAt || new Date().toISOString()});
    }
    await loadAiMessages().catch(()=>{});
  }
  catch(e){
    // Do not reload chat from the database after an AI error.
    // The old build reloaded here, which erased the visible message and looked like the AI reset.
    state.aiMessages.push({role:'assistant',content:e.message || t('aiDisabled'),created_at:new Date().toISOString(), error:true});
  }
  finally{
    state.aiBusy=false;
    render();
    setTimeout(()=>{const box=$('#chatBox'); if(box) box.scrollTop=box.scrollHeight;},50);
  }
};

function modalHtml(){
  if(!state.modal) return '';
  const m=state.modal;
  const title = {recipient:t('careRecipient'),member:t('addMember'),medication:t('addMedication'),task:t('addTask'),appointment:t('addAppointment'),journal:t('addJournal')}[m] || '';
  const body = m==='recipient'?recipientFormHtml():m==='member'?memberFormHtml():m==='medication'?medFormHtml():m==='task'?taskFormHtml():m==='appointment'?apptFormHtml():journalFormHtml();
  return `<div class="modal-backdrop" onclick="if(event.target.className==='modal-backdrop')closeModal()"><div class="modal glass"><div class="modal-head"><h2>${title}</h2><button class="icon-btn" onclick="closeModal()">×</button></div><form onsubmit="saveModal(event,'${m}')">${body}<div id="modalError"></div><div class="modal-actions"><button class="btn" type="button" onclick="closeModal()">${t('cancel')}</button><button class="btn primary" type="submit">${t('save')}</button></div></form></div></div>`;
}
function getEdit(){ return state.editItem || {}; }
function recipientFormHtml(){ const p=state.data?.careRecipient||{}; return `<div class="form-grid">${field2('recipientName',t('recipientName'),p.recipient_name,true,t('recipientNameHelp'))}${field2('recipientAge',t('age'),p.recipient_age,'number','')}${field2('relationship',t('relationship'),p.relationship,false,'Example: mother, father, grandmother, patient.')}${field2('livingSituation',t('livingSituation'),p.living_situation,false,'Independent / with family / care facility.')}${field2('location',t('location'),p.location,false,'')}${field2('gpName',t('gpName'),p.gp_name,false,'')}${field2('gpPhone',t('gpPhone'),p.gp_phone,false,'')}${textArea('conditions',t('conditions'),p.conditions,'Example: diabetes, heart disease, mobility issues.')}${textArea('allergies',t('allergies'),p.allergies,'Known allergies, or write none.')}</div>`; }
function memberFormHtml(){ const x=getEdit(); return `<div class="form-grid">${field2('name',t('memberName'),x.name,true,t('memberNameHelp'))}${field2('email',t('memberEmail')+' *',x.email,'email',t('memberEmailHelp'))}${field2('phone',`${t('memberPhone')} (${t('optional')})`,x.phone,false,'')}${selectField('role',t('role'),x.role||'supporting',[[ 'primary',t('primary')],[ 'supporting',t('supporting')],[ 'remote',t('remote')]],t('roleHelp'))}${textArea('notes',t('notes'),x.notes,'Optional notes about availability or responsibility.')}</div>`; }
function medFormHtml(){ const x=getEdit(); return `<div class="form-grid">${field2('name',t('medName'),x.name,true,t('medNameHelp'))}${field2('dosage',t('dosage'),x.dosage,false,t('dosageHelp'))}${field2('frequency',t('frequency'),x.frequency,false,t('frequencyHelp'))}${field2('purpose',t('purpose'),x.purpose,false,t('purposeHelp'))}${field2('prescribingDoctor',t('doctor'),x.prescribing_doctor,false,'')}${field2('refillDate',t('refillDate'),x.refill_date,'date','')}${textArea('notes',t('notes'),x.notes,'Any safe notes. This app does not replace a doctor.')}</div>`; }
function taskFormHtml(){ const x=getEdit(); const members=state.data?.familyMembers||[]; return `<div class="form-grid">${field2('title',t('taskTitle'),x.title,true,t('taskTitleHelp'))}${selectField('assignedToMemberId',t('assignedTo'),x.assigned_to_member_id||'', [['','Unassigned'],...members.map(m=>[m.id,m.name])], 'Choose from the family members you added manually.')}${field2('dueDate',t('dueDate'),x.due_date,'date','')}${selectField('status',t('status'),x.status||'todo', [['todo','To Do'],['progress','In Progress'],['done','Done']], '')}${selectField('category',t('category'),x.category||'practical', [['medical','Medical'],['practical','Practical'],['social','Social'],['financial','Financial'],['household','Household'],['transport','Transport'],['other','Other']], '')}${selectField('priority',t('priority'),x.priority||'normal', [['normal','Normal'],['high','High'],['urgent','Urgent'],['low','Low']], '')}${selectField('recurring',t('recurring'),x.recurring||'none', [['none','None'],['daily','Daily'],['weekly','Weekly'],['monthly','Monthly']], '')}${textArea('description',t('description'),x.description,'More details for the assigned member.')}</div>`; }
function apptFormHtml(){ const x=getEdit(); const members=state.data?.familyMembers||[]; return `<div class="form-grid">${field2('title',t('apptTitle'),x.title,true,'Example: Cardiology check-up.')}${field2('appointmentDateTime',t('dateTime'),x.appointment_datetime,'datetime-local','')}${field2('doctorName',t('doctor'),x.doctor_name,false,'')}${field2('location',t('location'),x.location,false,'Clinic, hospital, or address.')}${selectField('accompaniedByMemberId',t('accompaniedBy'),x.accompanied_by_member_id||'', [['','Unassigned'],...members.map(m=>[m.id,m.name])], 'Choose from family members you added.')}${textArea('notes',t('notes'),x.notes,'Appointment notes or questions to ask.')}</div>`; }
function journalFormHtml(){ return `${textArea('entryText',t('journalText'),' ',t('journalHelp'))}`; }
function field2(id,label,value='',typeOrReq=false,help=''){
  let type='text', req=false; if(typeOrReq===true){req=true}else if(typeof typeOrReq==='string'){type=typeOrReq; req=label.includes('*')}
  const cleanLabel = String(label).replace(/ \*$/,''); return `<label class="field"><span>${esc(cleanLabel)}${req?' *':''}</span><div class="input-wrap"><input id="${id}" name="${id}" type="${type}" value="${esc(value||'')}" ${req?'required':''}></div>${help?`<small>${esc(help)}</small>`:''}</label>`;
}
function textArea(id,label,value='',help=''){ return `<label class="field" style="grid-column:1/-1"><span>${esc(label)}</span><div class="input-wrap"><textarea id="${id}" name="${id}">${esc(value||'')}</textarea></div>${help?`<small>${esc(help)}</small>`:''}</label>`; }
function selectField(id,label,value,options,help=''){ return `<label class="field"><span>${esc(label)}</span><div class="input-wrap"><select id="${id}" name="${id}">${options.map(([v,l])=>`<option value="${esc(v)}" ${String(value)===String(v)?'selected':''}>${esc(l)}</option>`).join('')}</select></div>${help?`<small>${esc(help)}</small>`:''}</label>`; }

window.openModal=(type)=>{state.modal=type; state.editItem=null; render();};
window.closeModal=()=>{state.modal=null; state.editItem=null; render();};
window.editEntity=(type,id)=>{ const map={member:'familyMembers',medication:'medications',task:'tasks',appointment:'appointments'}; state.editItem=(state.data[map[type]]||[]).find(x=>x.id===id)||{}; state.modal=type; render(); };
window.saveModal=async(ev,type)=>{ ev.preventDefault(); const fd=new FormData(ev.target); const obj=Object.fromEntries(fd.entries()); try{ if(type==='recipient') await saveRecipient(obj); else await saveEntity(type,obj); closeModal(); showToast(t('saved')); await loadData(); render(); }catch(e){ $('#modalError').innerHTML=`<div class="error">${esc(e.message)}</div>`; } };
async function saveRecipient(obj=null){ if(!obj){ const form=$('section form'); obj=Object.fromEntries(new FormData(form).entries()); } await api('/api/care-recipient',{method:'POST',body:obj}); const me=await api('/api/auth/me'); state.user=me.user; await loadData(); showToast(t('saved')); go('dashboard'); }
async function saveEntity(type,obj){ const route={member:'members',medication:'medications',task:'tasks',appointment:'appointments',journal:'journal'}[type]; const id=state.editItem?.id; await api(`/api/${route}${id?'/'+id:''}`,{method:id?'PUT':'POST',body:obj}); }
window.deleteEntity=async(route,id)=>{ if(!confirm('Delete this item?')) return; await api(`/api/${route}/${id}`,{method:'DELETE'}); await loadData(); showToast(t('deleted')); render(); };

function render(){
  document.body.classList.toggle('rtl', state.lang==='ar');
  document.documentElement.dir = state.lang==='ar'?'rtl':'ltr';
  state.route = routeFromHash();
  let html='';
  if(!state.user){ if(state.route==='signup') html=authPage('signup'); else if(state.route==='login') html=authPage('login'); else html=landing(); }
  else {
    if(state.route==='onboarding') html=onboardingPage();
    else if(state.route==='family') html=familyPage();
    else if(state.route==='medications') html=medicationsPage();
    else if(state.route==='tasks') html=tasksPage();
    else if(state.route==='appointments') html=appointmentsPage();
    else if(state.route==='journal') html=journalPage();
    else if(state.route==='ai') html=aiPage();
    else if(state.route==='notifications') html=notificationsPage();
    else if(state.route==='settings') html=settingsPage();
    else html=dashboard();
  }
  app.innerHTML = html + modalHtml();
  setTimeout(()=>{const box=$('#chatBox'); if(box) box.scrollTop=box.scrollHeight;},0);
}

window.addEventListener('hashchange', ensureRoute);
window.setLang=setLang; window.go=go; window.globalSearch=(v)=>{};
boot();
