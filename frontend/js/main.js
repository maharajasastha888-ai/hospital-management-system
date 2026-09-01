// Utility functions
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function formatDateTime(dateStr) {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleString('en-IN');
}

function formatCurrency(amount) {
    return `$${parseFloat(amount || 0).toFixed(2)}`;
}

function getStatusBadge(status) {
    const map = {
        'scheduled': 'badge-info',
        'completed': 'badge-success',
        'cancelled': 'badge-danger',
        'paid': 'badge-success',
        'unpaid': 'badge-warning',
        'partial': 'badge-warning',
        'active': 'badge-success',
        'discharged': 'badge-info',
        'pending': 'badge-warning',
        'in_progress': 'badge-info',
        'available': 'badge-success',
        'occupied': 'badge-danger'
    };
    const cls = map[status] || 'badge-info';
    return `<span class="badge ${cls}">${status}</span>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function loadComponent(selector, url) {
    return fetch(url).then(r => r.text()).then(html => {
        document.querySelector(selector).innerHTML = html;
    });
}

function populateSelect(selectId, items, valueKey = 'id', labelKey = 'name', placeholder = 'Select...') {
    const select = document.getElementById(selectId);
    if (!select) return;
    select.innerHTML = `<option value="">${placeholder}</option>`;
    items.forEach(item => {
        const opt = document.createElement('option');
        opt.value = item[valueKey];
        opt.textContent = item[labelKey];
        select.appendChild(opt);
    });
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    const icon = document.querySelector('.dark-mode-toggle i');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// Initialize dark mode
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Initialize sidebar
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.dataset.page === currentPage.replace('.html', '')) {
            item.classList.add('active');
        }
    });
});
