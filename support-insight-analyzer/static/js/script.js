// Global functions for the Support Insight Analyzer

function runAnalysis() {
    const button = document.getElementById('runAnalysisBtn');
    const originalText = button.innerHTML;
    
    button.innerHTML = '<span class="loading"></span> Running Analysis...';
    button.disabled = true;

    fetch('/run-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redirect to results page or show modal
            showAnalysisResults(data.results);
        } else {
            alert('Analysis failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Analysis failed: ' + error);
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function showAnalysisResults(results) {
    // Create a modal or redirect to show results
    const resultsStr = JSON.stringify(results, null, 2);
    alert('Analysis completed! Check console for results or implement a results page.');
    console.log('Analysis Results:', results);
    
    // You can implement a modal here to show results
    // For now, we'll just log to console
}

// Chart initialization functions
function initializeSentimentChart(sentimentData) {
    const ctx = document.getElementById('sentimentChart').getContext('2d');
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Neutral', 'Negative'],
            datasets: [{
                data: [
                    sentimentData.total_positive,
                    sentimentData.total_neutral,
                    sentimentData.total_negative
                ],
                backgroundColor: [
                    '#198754',
                    '#0dcaf0',
                    '#dc3545'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function initializeTrendsChart(trendsData) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    const categories = Object.keys(trendsData.category_trends);
    const counts = Object.values(trendsData.category_trends);
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Tickets by Category',
                data: counts,
                backgroundColor: '#0d6efd'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Utility functions
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function getPriorityBadge(priority) {
    const badges = {
        'Critical': 'badge-critical',
        'High': 'badge-high',
        'Medium': 'badge-medium',
        'Low': 'badge-low'
    };
    return badges[priority] || 'badge-secondary';
}