/**
 * Omega Platform Dashboard Utilities
 */

class DashboardUtils {
    constructor() {
        this.autoRefreshInterval = null;
        this.isRefreshing = false;
    }
    
    // Format bytes to human readable
    formatBytes(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    }
    
    // Format time duration
    formatDuration(seconds) {
        if (seconds < 60) {
            return `${seconds}s`;
        } else if (seconds < 3600) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return `${minutes}m ${remainingSeconds}s`;
        } else {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            return `${hours}h ${minutes}m`;
        }
    }
    
    // Create a debounced function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Get color based on status
    getStatusColor(status) {
        const colors = {
            'active': '#10B981',
            'running': '#3B82F6',
            'warning': '#F59E0B',
            'error': '#EF4444',
            'inactive': '#6B7280',
            'completed': '#8B5CF6'
        };
        return colors[status.toLowerCase()] || '#6B7280';
    }
    
    // Create a progress bar element
    createProgressBar(percentage, color = '#3B82F6') {
        const container = document.createElement('div');
        container.className = 'w-full bg-gray-700 rounded-full h-2';
        
        const bar = document.createElement('div');
        bar.className = 'h-2 rounded-full';
        bar.style.width = `${percentage}%`;
        bar.style.backgroundColor = color;
        
        container.appendChild(bar);
        return container;
    }
}

// Export for use in browser
if (typeof window !== 'undefined') {
    window.DashboardUtils = new DashboardUtils();
}

/**
 * Chart.js configuration for Omega Platform
 */
class DashboardCharts {
    static getDefaultOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#9CA3AF',
                        font: {
                            family: "'Inter', sans-serif"
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(17, 24, 39, 0.9)',
                    titleColor: '#F3F4F6',
                    bodyColor: '#D1D5DB',
                    borderColor: '#374151',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: {
                        color: '#374151'
                    },
                    ticks: {
                        color: '#9CA3AF'
                    }
                },
                y: {
                    grid: {
                        color: '#374151'
                    },
                    ticks: {
                        color: '#9CA3AF'
                    }
                }
            }
        };
    }
    
    static createDetectionRateChart(ctx, data) {
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Detection Rate',
                    data: data.values || [85, 88, 82, 90, 87, 89, 91],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: this.getDefaultOptions()
        });
    }
    
    static createThreatDistributionChart(ctx, data) {
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels || ['APT', 'Ransomware', 'Insider', 'Phishing', 'DDoS'],
                datasets: [{
                    data: data.values || [25, 30, 15, 20, 10],
                    backgroundColor: [
                        '#EF4444',
                        '#F59E0B',
                        '#8B5CF6',
                        '#3B82F6',
                        '#10B981'
                    ]
                }]
            },
            options: {
                ...this.getDefaultOptions(),
                cutout: '70%'
            }
        });
    }
}
