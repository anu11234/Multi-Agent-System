import json
import pandas as pd
from datetime import datetime, timedelta
import os
import logging

class MemoryManager:
    def __init__(self, db_path='memory/support_data.json'):
        self.db_path = db_path
        self.logger = logging.getLogger('memory_manager')
        self.initialize_memory()
    
    def initialize_memory(self):
        """Initialize memory database with sample data"""
        if not os.path.exists(self.db_path):
            sample_data = {
                "tickets": self._generate_sample_tickets(),
                "analyses": [],
                "trends": [],
                "system_status": {
                    "last_analysis": None,
                    "total_tickets_processed": 0,
                    "system_uptime": "100%"
                }
            }
            self._save_data(sample_data)
            self.logger.info("Local memory database initialized")
    
    def _generate_sample_tickets(self):
        """Generate sample support tickets for demonstration"""
        tickets = []
        issues = [
            "Login problems", "Payment failed", "Feature not working", 
            "Account verification", "Billing inquiry", "Performance issues",
            "Mobile app crash", "Data sync problem", "UI/UX feedback"
        ]
        
        priorities = ["Low", "Medium", "High", "Critical"]
        statuses = ["Open", "In Progress", "Resolved", "Closed"]
        
        for i in range(100):
            ticket = {
                "id": f"TKT-{1000 + i}",
                "subject": f"{issues[i % len(issues)]} - Case {i}",
                "description": f"Customer reported issue with {issues[i % len(issues)].lower()}. Requires attention.",
                "priority": priorities[i % len(priorities)],
                "status": statuses[i % len(statuses)],
                "created_date": (datetime.now() - timedelta(days=i % 30)).strftime("%Y-%m-%d"),
                "customer_sentiment": ["Positive", "Neutral", "Negative"][i % 3],
                "category": ["Technical", "Billing", "Account", "Feature"][i % 4],
                "agent_assigned": f"Agent_{(i % 5) + 1}"
            }
            tickets.append(ticket)
        
        return tickets
    
    def _save_data(self, data):
        """Save data to JSON file"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_data(self):
        """Load data from JSON file"""
        with open(self.db_path, 'r') as f:
            return json.load(f)
    
    def get_recent_tickets(self, days=7):
        """Get recent tickets from the last N days"""
        data = self._load_data()
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        recent_tickets = [
            ticket for ticket in data['tickets'] 
            if ticket['created_date'] >= cutoff_date
        ]
        return recent_tickets
    
    def get_ticket_statistics(self):
        """Get ticket statistics"""
        data = self._load_data()
        df = pd.DataFrame(data['tickets'])
        
        stats = {
            'total_tickets': len(data['tickets']),
            'open_tickets': len([t for t in data['tickets'] if t['status'] in ['Open', 'In Progress']]),
            'critical_tickets': len([t for t in data['tickets'] if t['priority'] == 'Critical']),
            'sentiment_distribution': df['customer_sentiment'].value_counts().to_dict(),
            'category_distribution': df['category'].value_counts().to_dict(),
            'priority_distribution': df['priority'].value_counts().to_dict()
        }
        
        return stats
    
    def save_analysis(self, analysis_data):
        """Save analysis results"""
        data = self._load_data()
        analysis_data['timestamp'] = datetime.now().isoformat()
        analysis_data['id'] = f"ANA-{len(data['analyses']) + 1}"
        data['analyses'].append(analysis_data)
        self._save_data(data)
        return analysis_data['id']
    
    def get_historical_analyses(self):
        """Get all historical analyses"""
        data = self._load_data()
        return data['analyses']