from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'minimal-secret-key'

class SimpleMemoryManager:
    def __init__(self):
        self.tickets = self._generate_sample_tickets()
    
    def _generate_sample_tickets(self):
        """Generate sample support tickets"""
        tickets = []
        issues = ["Login problems", "Payment failed", "Feature not working"]
        priorities = ["Low", "Medium", "High", "Critical"]
        
        for i in range(50):
            ticket = {
                "id": f"TKT-{1000 + i}",
                "subject": f"{issues[i % len(issues)]} - Case {i}",
                "priority": priorities[i % len(priorities)],
                "status": random.choice(["Open", "Resolved"]),
                "created_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "category": random.choice(["Technical", "Billing", "Account"])
            }
            tickets.append(ticket)
        
        return tickets
    
    def get_recent_tickets(self, days=7):
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return [t for t in self.tickets if t['created_date'] >= cutoff_date][:10]
    
    def get_ticket_statistics(self):
        return {
            'total_tickets': len(self.tickets),
            'open_tickets': len([t for t in self.tickets if t['status'] == 'Open']),
            'critical_tickets': len([t for t in self.tickets if t['priority'] == 'Critical'])
        }

# Initialize memory manager
memory_manager = SimpleMemoryManager()

@app.route('/')
def index():
    stats = memory_manager.get_ticket_statistics()
    return f"""
    <html>
        <head>
            <title>Support Insight Analyzer - Minimal Version</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <nav class="navbar navbar-dark bg-dark">
                <div class="container">
                    <span class="navbar-brand">Support Insight Analyzer</span>
                </div>
            </nav>
            <div class="container mt-4">
                <div class="card">
                    <div class="card-header">
                        <h3>System Status</h3>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-success">✅ System Ready</div>
                        <div class="row text-center">
                            <div class="col-md-4">
                                <h4>{stats['total_tickets']}</h4>
                                <p>Total Tickets</p>
                            </div>
                            <div class="col-md-4">
                                <h4>{stats['open_tickets']}</h4>
                                <p>Open Tickets</p>
                            </div>
                            <div class="col-md-4">
                                <h4>{stats['critical_tickets']}</h4>
                                <p>Critical Tickets</p>
                            </div>
                        </div>
                        <a href="/analysis" class="btn btn-primary">Run Analysis</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/analysis')
def analysis():
    recent_tickets = memory_manager.get_recent_tickets()
    stats = memory_manager.get_ticket_statistics()
    
    tickets_html = ""
    for ticket in recent_tickets:
        badge_color = "danger" if ticket['priority'] == 'Critical' else "warning" if ticket['priority'] == 'High' else "info"
        tickets_html += f"""
        <tr>
            <td>{ticket['id']}</td>
            <td>{ticket['subject']}</td>
            <td><span class="badge bg-{badge_color}">{ticket['priority']}</span></td>
            <td>{ticket['category']}</td>
        </tr>
        """
    
    return f"""
    <html>
        <head>
            <title>Analysis - Support Insight Analyzer</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <nav class="navbar navbar-dark bg-dark">
                <div class="container">
                    <span class="navbar-brand">Support Insight Analyzer</span>
                </div>
            </nav>
            <div class="container mt-4">
                <div class="card">
                    <div class="card-header">
                        <h3>Real-time Analysis</h3>
                    </div>
                    <div class="card-body">
                        <h5>Recent Tickets (Last 7 days)</h5>
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Subject</th>
                                    <th>Priority</th>
                                    <th>Category</th>
                                </tr>
                            </thead>
                            <tbody>
                                {tickets_html}
                            </tbody>
                        </table>
                        <button class="btn btn-success" onclick="runAnalysis()">Run AI Analysis</button>
                        <div id="results" class="mt-3"></div>
                    </div>
                </div>
            </div>
            <script>
                function runAnalysis() {{
                    document.getElementById('results').innerHTML = `
                        <div class="alert alert-success">
                            <h5>Analysis Complete!</h5>
                            <p>Analyzed {len(recent_tickets)} recent tickets</p>
                            <p>Found {stats['critical_tickets']} critical issues needing attention</p>
                            <p>System is operating normally</p>
                        </div>
                    `;
                }}
            </script>
        </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 Starting Support Insight Analyzer (Minimal Version)")
    print("📍 Access at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)