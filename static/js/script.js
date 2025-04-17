const ctx = document.getElementById('admissionChart').getContext('2d');

const admissionChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov', 'Déc'],
        datasets: [
            {
                label: 'Admissions',
                data: [140, 180, 220, 160, 168, 130, 150],
                borderColor: '#23a34c',
                backgroundColor: 'rgba(35, 163, 76, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#23a34c'
            },
            {
                label: 'Sorties',
                data: [100, 130, 150, 120, 143, 110, 105],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true,
                pointRadius: 5,
                pointBackgroundColor: '#3b82f6'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#333',
                    font: {
                        size: 13
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `${context.dataset.label}: ${context.parsed.y}`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 50
                },
                grid: {
                    color: '#eee'
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        }
    }
});
