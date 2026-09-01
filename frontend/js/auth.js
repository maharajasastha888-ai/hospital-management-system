function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) {
        const div = document.createElement('div');
        div.id = 'toast-container';
        div.className = 'toast-container';
        document.body.appendChild(div);
    }
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    document.getElementById('toast-container').appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function setToken(token) {
    localStorage.setItem('token', token);
    api.token = token;
}

function getToken() {
    return localStorage.getItem('token');
}

function clearToken() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    api.token = null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function getUser() {
    const data = localStorage.getItem('user');
    return data ? JSON.parse(data) : null;
}

function isLoggedIn() {
    return !!getToken();
}

function getDashboardUrl(role) {
    const urls = {
        'admin': '/pages/admin/dashboard.html',
        'doctor': '/pages/doctor/dashboard.html',
        'receptionist': '/pages/receptionist/dashboard.html',
        'patient': '/pages/patient/dashboard.html',
        'pharmacist': '/pages/pharmacist/dashboard.html',
        'lab_technician': '/pages/lab/dashboard.html'
    };
    return urls[role] || '/pages/login.html';
}

async function login(username, password) {
    const data = await api.post('/auth/login', { username, password });
    setToken(data.token);
    setUser(data.user);
    return data;
}

function logout() {
    clearToken();
    window.location.href = '/pages/login.html';
}

function redirectToDashboard() {
    const user = getUser();
    if (user) {
        window.location.href = getDashboardUrl(user.role);
    } else {
        window.location.href = '/pages/login.html';
    }
}

async function checkAuth() {
    if (!isLoggedIn()) {
        window.location.href = '/pages/login.html';
        return null;
    }
    try {
        const user = await api.get('/auth/me');
        setUser(user);
        return user;
    } catch {
        clearToken();
        window.location.href = '/pages/login.html';
        return null;
    }
}
