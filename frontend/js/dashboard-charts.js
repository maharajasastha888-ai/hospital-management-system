let revenueChart = null;
let patientChart = null;

async function initDashboardCharts() {
    try {
        // Monthly Revenue Chart
        const revenueData = await api.get('/admin/revenue/monthly');
        const ctx1 = document.getElementById('revenueChart');
        if (ctx1) {
            const labels = revenueData.map(d => d.month).reverse();
            const data = revenueData.map(d => d.revenue).reverse();
            if (revenueChart) revenueChart.destroy();
            revenueChart = new Chart(ctx1.getContext('2d'), {
                type: 'bar',
                data: {
                    labels,
                    datasets: [{
                        label: 'Revenue ($)',
                        data,
                        backgroundColor: 'rgba(52, 152, 219, 0.6)',
                        borderColor: 'rgba(52, 152, 219, 1)',
                        borderWidth: 2,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        title: { display: true, text: 'Monthly Revenue' }
                    },
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        // Patient Chart
        const ctx2 = document.getElementById('patientChart');
        if (ctx2) {
            if (patientChart) patientChart.destroy();
            patientChart = new Chart(ctx2.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: ['OPD', 'IPD', 'Emergency'],
                    datasets: [{
                        data: [65, 20, 15],
                        backgroundColor: [
                            'rgba(39, 174, 96, 0.8)',
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(231, 76, 60, 0.8)'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        title: { display: true, text: 'Patient Distribution' }
                    }
                }
            });
        }
    } catch (err) {
        console.error('Failed to load charts:', err);
    }
}
