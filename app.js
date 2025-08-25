document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:8000'; // URL BAZË PËR API-NË

    // Referencat e elementeve
    const authContainer = document.getElementById('auth-container');
    const mainContent = document.getElementById('main-content');
    const seksioniLogin = document.getElementById('seksioni-login');
    const seksioniRegjistrimit = document.getElementById('seksioni-regjistrimit');
    const seksioniPerdoruesit = document.getElementById('seksioni-perdoruesit');
    const listaEFondeve = document.getElementById('lista-e-fondeve');
    const listaInvestimeve = document.getElementById('lista-e-investimeve');
    
    // Referencat për dritaren modale
    const investModalEl = document.getElementById('investModal');
    const investModal = new bootstrap.Modal(investModalEl);
    const modalFondName = document.getElementById('modalFondName');
    const investFondId = document.getElementById('investFondId');
    const investForm = document.getElementById('investForm');

    function perditesoUI() {
        const accessToken = localStorage.getItem('accessToken');
        if (accessToken) {
            try {
                const perdoruesi = parseJwt(accessToken);
                document.getElementById('mesazhi-pershendetes').textContent = `Mirë se erdhe, ${perdoruesi.username}!`;
                
                authContainer.style.display = 'none';
                mainContent.style.display = 'block';
                seksioniPerdoruesit.style.display = 'flex';
                
                shfaqInvestimetPersonale();
            } catch (e) {
                localStorage.removeItem('accessToken');
                perditesoUI();
            }
        } else {
            authContainer.style.display = 'block';
            mainContent.style.display = 'none';
            seksioniPerdoruesit.style.display = 'none';
        }
    }

    document.getElementById('switchToRegister').addEventListener('click', (e) => { e.preventDefault(); seksioniLogin.style.display = 'none'; seksioniRegjistrimit.style.display = 'block'; });
    document.getElementById('switchToLogin').addEventListener('click', (e) => { e.preventDefault(); seksioniRegjistrimit.style.display = 'none'; seksioniLogin.style.display = 'block'; });
    document.getElementById('logoutButton').addEventListener('click', () => { localStorage.removeItem('accessToken'); perditesoUI(); });

    async function shfaqListenEFondeve() {
        try {
            const response = await fetch(`${API_BASE_URL}/api/fondet/`);
            const fondet = await response.json();
            listaEFondeve.innerHTML = '';
            fondet.forEach(fond => {
                const fondItem = document.createElement('a');
                fondItem.className = 'list-group-item list-group-item-action';
                fondItem.href = '#';
                fondItem.innerHTML = `<div class="d-flex w-100 justify-content-between"><h5 class="mb-1">${fond.emri}</h5><button class="btn btn-sm btn-success investo-btn">Investo</button></div><p class="mb-1">${fond.pershkrimi}</p>`;
                fondItem.querySelector('.investo-btn').addEventListener('click', (e) => {
                    e.stopPropagation();
                    if (!localStorage.getItem('accessToken')) return alert('Ju duhet të jeni i loguar!');
                    modalFondName.textContent = fond.emri;
                    investFondId.value = fond.id;
                    document.getElementById('investMessage').textContent = '';
                    investModal.show();
                });
                listaEFondeve.appendChild(fondItem);
            });
        } catch (e) {
            listaEFondeve.innerHTML = '<div class="alert alert-danger">Gabim gjatë lidhjes me serverin.</div>';
        }
    }

    async function shfaqInvestimetPersonale() {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) return;
        try {
            const response = await fetch(`${API_BASE_URL}/api/investimet-e-mia/`, { headers: { 'Authorization': `Bearer ${accessToken}` } });
            if (response.status === 401) { localStorage.removeItem('accessToken'); perditesoUI(); return; }
            const investimet = await response.json();
            listaInvestimeve.innerHTML = '';
            if (investimet.length === 0) { listaInvestimeve.innerHTML = '<div class="alert alert-info">Nuk keni asnjë investim aktiv.</div>'; return; }
            investimet.forEach(investim => {
                const divInvestimi = document.createElement('div');
                divInvestimi.className = 'card card-body mb-2';
                const fitimiClass = investim.fitimi >= 0 ? 'text-success' : 'text-danger';
                divInvestimi.innerHTML = `
                    <h6>${investim.fondi}</h6>
                    <p class="mb-1 small">Investuar: ${investim.vlera_totale_investuar} EUR</p>
                    <p class="mb-1">Vlera Aktuale: <strong>${investim.vlera_aktuale} EUR</strong></p>
                    <p class="mb-0">Fitimi / Humbja: <strong class="${fitimiClass}">${investim.fitimi} EUR</strong></p>
                `;
                listaInvestimeve.appendChild(divInvestimi);
            });
        } catch(e) { console.error(e); }
    }
    
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const msgEl = document.getElementById('loginMessage');
        msgEl.textContent = '';
        const username = e.target.username.value;
        const password = e.target.password.value;
        try {
            const response = await fetch(`${API_BASE_URL}/api/token/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, password }) });
            if (!response.ok) throw new Error('Kredenciale të gabuara!');
            const data = await response.json();
            localStorage.setItem('accessToken', data.access);
            perditesoUI();
        } catch (error) { msgEl.textContent = error.message; }
    });

    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const msgEl = document.getElementById('registerMessage');
        msgEl.textContent = 'Duke u regjistruar...';
        const username = e.target.elements['reg-username'].value;
        const email = e.target.elements['reg-email'].value;
        const password = e.target.elements['reg-password'].value;
        try {
            const response = await fetch(`${API_BASE_URL}/api/regjistrohu/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username, email, password }) });
            const data = await response.json();
            if (!response.ok) throw new Error(JSON.stringify(data));
            msgEl.className = 'text-success mt-2';
            msgEl.textContent = 'Regjistrimi u krye me sukses! Tani mund të bëni login.';
            e.target.reset();
        } catch (error) { msgEl.className = 'text-danger mt-2'; msgEl.textContent = `Gabim: ${error.message}`; }
    });

    investForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const msgEl = document.getElementById('investMessage');
        msgEl.textContent = 'Duke procesuar...';
        const accessToken = localStorage.getItem('accessToken');
        const shuma = document.getElementById('investShuma').value;
        const fond_id = investFondId.value;
        try {
            const response = await fetch(`${API_BASE_URL}/api/investo/`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${accessToken}` }, body: JSON.stringify({ fond_id: parseInt(fond_id), shuma }) });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || JSON.stringify(data));
            msgEl.className = 'text-success mt-2';
            msgEl.textContent = data.mesazhi;
            event.target.reset();
            shfaqInvestimetPersonale();
            setTimeout(() => { investModal.hide(); }, 1500); // Mbyll modalin pas 1.5 sekonda
        } catch (error) { msgEl.className = 'text-danger mt-2'; msgEl.textContent = `Gabim: ${error.message}`; }
    });

    function parseJwt(token) {
        try { return JSON.parse(atob(token.split('.')[1])); } catch (e) { return null; }
    }

    // Thirrjet fillestare
    shfaqListenEFondeve();
    perditesoUI();
});