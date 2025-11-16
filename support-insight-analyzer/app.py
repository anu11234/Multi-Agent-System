from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import random
import json
import time
import threading
from collections import deque
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dynamic-ai-agent-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Global variables for real-time data
live_tickets = deque(maxlen=100)
analysis_results = {}
system_metrics = {
    'tickets_processed': 0,
    'avg_response_time': 0,
    'customer_satisfaction': 0,
    'active_agents': 0
}

class RealTimeDataGenerator:
    def __init__(self):
        self.issues = [
            "Login authentication failed", "Payment gateway timeout", "Feature not responding",
            "Account verification pending", "Billing discrepancy", "Performance degradation",
            "Mobile app crashing on launch", "Data synchronization failed", "UI rendering issues",
            "API rate limiting", "Database connection timeout", "File upload failing"
        ]
        self.priorities = ["Low", "Medium", "High", "Critical"]
        self.categories = ["Technical", "Billing", "Account", "Feature", "Performance", "Security"]
        self.agents = ["AI_Agent_1", "AI_Agent_2", "AI_Agent_3", "Support_Agent_1", "Support_Agent_2"]
        self.sentiments = ["Positive", "Neutral", "Negative"]
        
    def generate_live_ticket(self):
        """Generate a realistic live support ticket"""
        issue = random.choice(self.issues)
        priority_weights = [0.15, 0.35, 0.35, 0.15]  # More medium/high, fewer critical/low
        priority = random.choices(self.priorities, weights=priority_weights)[0]
        
        ticket = {
            'id': f"TKT-{int(time.time())}{random.randint(100, 999)}",
            'subject': f"{issue} - Session_{random.randint(1000, 9999)}",
            'description': f"Customer experiencing {issue.lower()}. Additional context: {self.generate_description(issue)}",
            'priority': priority,
            'category': random.choice(self.categories),
            'status': 'Open',
            'customer_sentiment': random.choices(self.sentiments, weights=[0.3, 0.4, 0.3])[0],
            'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'agent_assigned': random.choice(self.agents),
            'response_time': random.randint(5, 120),  # minutes
            'satisfaction_score': random.randint(1, 10),
            'urgency_level': self.priorities.index(priority) + 1
        }
        return ticket
    
    def generate_description(self, issue):
        descriptions = {
            "Login authentication failed": "User unable to access account despite correct credentials. Multiple attempts made.",
            "Payment gateway timeout": "Transaction stuck at processing stage. Customer concerned about double charge.",
            "Feature not responding": "Specific functionality unresponsive. Tried refreshing and different browsers.",
            "Performance degradation": "System running slower than usual. Impacting daily operations significantly.",
            "Mobile app crashing": "Application crashes immediately after launch. Reinstall didn't resolve."
        }
        return descriptions.get(issue, "User requires immediate assistance with this issue.")

class DynamicAnalysisEngine:
    def __init__(self):
        self.trend_data = deque(maxlen=50)
        self.sentiment_history = deque(maxlen=100)
        
    def analyze_realtime_trends(self, tickets):
        """Dynamic trend analysis with live data"""
        if not tickets:
            return {}
            
        # Convert to DataFrame-like structure for analysis
        categories = [t['category'] for t in tickets]
        priorities = [t['priority'] for t in tickets]
        sentiments = [t['customer_sentiment'] for t in tickets]
        
        # Real-time trend detection
        current_trends = {
            'rising_issues': self.detect_rising_issues(categories),
            'sentiment_trend': self.analyze_sentiment_trend(sentiments),
            'priority_distribution': self.calculate_priority_distribution(priorities),
            'response_metrics': self.calculate_response_metrics(tickets),
            'predicted_volume': self.predict_ticket_volume(tickets)
        }
        
        self.trend_data.append({
            'timestamp': datetime.now(),
            'trends': current_trends
        })
        
        return current_trends
    
    def detect_rising_issues(self, categories):
        """Detect issues that are increasing in frequency"""
        from collections import Counter
        category_counts = Counter(categories)
        
        rising = []
        for category, count in category_counts.most_common(3):
            if count >= 2:  # Threshold for rising issue
                trend = "Rapidly Increasing" if count > 5 else "Increasing"
                rising.append({
                    'category': category,
                    'frequency': count,
                    'trend': trend,
                    'impact_level': 'High' if count > 8 else 'Medium'
                })
        return rising
    
    def analyze_sentiment_trend(self, sentiments):
        """Analyze real-time sentiment trends"""
        sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
        for sentiment in sentiments:
            sentiment_counts[sentiment] += 1
            
        total = len(sentiments)
        if total == 0:
            return {'trend': 'Stable', 'score': 0}
            
        # Calculate sentiment score (-1 to 1)
        score = (sentiment_counts['Positive'] - sentiment_counts['Negative']) / total
        
        if score > 0.1:
            trend = "Improving"
        elif score < -0.1:
            trend = "Deteriorating"
        else:
            trend = "Stable"
            
        return {
            'trend': trend,
            'score': round(score, 3),
            'positive': sentiment_counts['Positive'],
            'negative': sentiment_counts['Negative'],
            'neutral': sentiment_counts['Neutral']
        }
    
    def calculate_priority_distribution(self, priorities):
        distribution = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for priority in priorities:
            distribution[priority] += 1
        return distribution
    
    def calculate_response_metrics(self, tickets):
        if not tickets:
            return {'avg_response_time': 0, 'resolution_rate': 0}
            
        response_times = [t.get('response_time', 0) for t in tickets]
        resolved = len([t for t in tickets if t.get('status') == 'Resolved'])
        
        return {
            'avg_response_time': round(sum(response_times) / len(response_times), 2),
            'resolution_rate': round(resolved / len(tickets) * 100, 1)
        }
    
    def predict_ticket_volume(self, tickets):
        """Simple prediction based on recent trends"""
        if len(self.trend_data) < 2:
            return {'predicted_tickets': len(tickets), 'confidence': 'Low'}
            
        recent_volume = [len(td['trends']['priority_distribution']) for td in list(self.trend_data)[-5:]]
        avg_volume = sum(recent_volume) / len(recent_volume)
        
        predicted = avg_volume * 1.1  # 10% increase prediction
        confidence = 'High' if len(recent_volume) >= 5 else 'Medium'
        
        return {
            'predicted_tickets': round(predicted),
            'confidence': confidence,
            'trend': 'Increasing' if predicted > avg_volume else 'Stable'
        }

# Initialize components
data_generator = RealTimeDataGenerator()
analysis_engine = DynamicAnalysisEngine()

def background_data_generator():
    """Background thread to generate live data"""
    while True:
        # Generate 1-3 new tickets randomly
        new_tickets = random.randint(1, 3)
        for _ in range(new_tickets):
            ticket = data_generator.generate_live_ticket()
            live_tickets.append(ticket)
            system_metrics['tickets_processed'] += 1
        
        # Update system metrics
        system_metrics['active_agents'] = random.randint(2, 5)
        system_metrics['customer_satisfaction'] = random.randint(75, 95)
        
        # Update some tickets status randomly
        for ticket in list(live_tickets)[-10:]:  # Only recent tickets
            if random.random() < 0.1:  # 10% chance to update status
                ticket['status'] = random.choice(['In Progress', 'Resolved'])
                ticket['customer_sentiment'] = random.choices(
                    ['Positive', 'Neutral', 'Negative'], 
                    weights=[0.6, 0.3, 0.1]
                )[0]
        
        time.sleep(random.randint(5, 15))  # Random interval between 5-15 seconds

# Start background thread
data_thread = threading.Thread(target=background_data_generator, daemon=True)
data_thread.start()

@app.route('/')
def index():
    """Dynamic dashboard with live metrics"""
    recent_tickets = list(live_tickets)[-10:] if live_tickets else []
    trends = analysis_engine.analyze_realtime_trends(recent_tickets)
    
    return render_template('index.html', 
                         metrics=system_metrics,
                         recent_tickets=recent_tickets,
                         trends=trends)

@app.route('/real-time-analysis')
def real_time_analysis():
    """Real-time analysis with live updates"""
    recent_tickets = list(live_tickets)[-20:] if live_tickets else []
    trends = analysis_engine.analyze_realtime_trends(recent_tickets)
    
    return render_template('real_time_analysis.html',
                         recent_tickets=recent_tickets[:10],
                         trends=trends,
                         metrics=system_metrics)

@app.route('/api/live-data')
def live_data():
    """API endpoint for live data updates"""
    recent_tickets = list(live_tickets)[-20:] if live_tickets else []
    trends = analysis_engine.analyze_realtime_trends(recent_tickets)
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'system_metrics': system_metrics,
        'recent_tickets': recent_tickets[:10],
        'trends': trends,
        'total_tickets': len(live_tickets),
        'active_trends': len(analysis_engine.trend_data)
    })

@app.route('/api/run-analysis', methods=['POST'])
def run_analysis():
    """Run comprehensive analysis on current data"""
    try:
        recent_tickets = list(live_tickets)[-50:] if live_tickets else []  # Last 50 tickets
        
        if not recent_tickets:
            return jsonify({'success': False, 'error': 'No data available for analysis'})
        
        # Comprehensive analysis
        trends = analysis_engine.analyze_realtime_trends(recent_tickets)
        
        # Generate insights
        insights = generate_dynamic_insights(trends, recent_tickets)
        
        # AI-powered recommendations
        recommendations = generate_ai_recommendations(insights, trends)
        
        analysis_result = {
            'success': True,
            'analysis_id': f"ANA-{int(time.time())}",
            'timestamp': datetime.now().isoformat(),
            'tickets_analyzed': len(recent_tickets),
            'time_period': 'Real-time (Live)',
            'trends': trends,
            'insights': insights,
            'recommendations': recommendations,
            'system_metrics': system_metrics
        }
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def generate_dynamic_insights(trends, tickets):
    """Generate dynamic insights based on current trends"""
    insights = []
    
    # Sentiment-based insights
    sentiment_trend = trends.get('sentiment_trend', {})
    if sentiment_trend.get('trend') == 'Deteriorating':
        insights.append({
            'type': 'warning',
            'title': 'Customer Sentiment Declining',
            'description': f"Negative sentiment is increasing ({sentiment_trend.get('negative', 0)} cases). Consider proactive outreach.",
            'priority': 'High',
            'confidence': 'High'
        })
    
    # Priority-based insights
    priority_dist = trends.get('priority_distribution', {})
    critical_tickets = priority_dist.get('Critical', 0)
    if critical_tickets > 3:
        insights.append({
            'type': 'critical',
            'title': 'Critical Issue Spike',
            'description': f"{critical_tickets} critical tickets requiring immediate attention.",
            'priority': 'Critical',
            'confidence': 'High'
        })
    
    # Response time insights
    response_metrics = trends.get('response_metrics', {})
    if response_metrics.get('avg_response_time', 0) > 60:
        insights.append({
            'type': 'warning',
            'title': 'Slow Response Times',
            'description': f"Average response time is {response_metrics['avg_response_time']} minutes. Consider adding support staff.",
            'priority': 'Medium',
            'confidence': 'Medium'
        })
    
    # Rising issues insights
    rising_issues = trends.get('rising_issues', [])
    if rising_issues:
        main_issue = rising_issues[0]
        insights.append({
            'type': 'info',
            'title': f"Emerging {main_issue['category']} Issues",
            'description': f"{main_issue['category']} issues are {main_issue['trend'].lower()} ({main_issue['frequency']} cases).",
            'priority': 'Medium',
            'confidence': main_issue['impact_level']
        })
    
    return insights

def generate_ai_recommendations(insights, trends):
    """Generate AI-powered recommendations"""
    recommendations = []
    
    for insight in insights:
        if insight['type'] == 'critical':
            recommendations.append({
                'action': 'Immediate Escalation Required',
                'description': f"Escalate {insight['title']} to senior team immediately",
                'timeline': 'Within 1 hour',
                'impact': 'High',
                'effort': 'Low'
            })
        elif insight['type'] == 'warning':
            recommendations.append({
                'action': 'Process Optimization',
                'description': f"Review and optimize process for {insight['title'].lower()}",
                'timeline': 'Within 24 hours',
                'impact': 'Medium',
                'effort': 'Medium'
            })
    
    # Add proactive recommendations
    predicted_volume = trends.get('predicted_volume', {})
    if predicted_volume.get('trend') == 'Increasing':
        recommendations.append({
            'action': 'Resource Planning',
            'description': f"Predicted increase in ticket volume. Plan additional resources.",
            'timeline': 'Next week',
            'impact': 'High',
            'effort': 'High'
        })
    
    return recommendations
@app.route('/historical-trends')
def historical_trends():
    """Historical trends dashboard"""
    # Get recent analyses (last 10)
    analyses = []
    if analysis_engine.trend_data:
        # Convert trend data to analysis format
        for i, trend in enumerate(list(analysis_engine.trend_data)[-10:]):
            analysis = {
                'id': f"ANA-{i+1}",
                'timestamp': trend['timestamp'].isoformat(),
                'tickets_analyzed': len(live_tickets) if live_tickets else 0,
                'sentiment_analysis': {
                    'total_positive': trend['trends']['sentiment_trend'].get('positive', 0),
                    'total_negative': trend['trends']['sentiment_trend'].get('negative', 0),
                    'total_neutral': trend['trends']['sentiment_trend'].get('neutral', 0)
                },
                'trend_analysis': {
                    'category_trends': trend['trends'].get('priority_distribution', {})
                },
                'key_insights': generate_dynamic_insights(trend['trends'], list(live_tickets)[-20:] if live_tickets else [])
            }
            analyses.append(analysis)
    
    return render_template('historical_trends.html', 
                         analyses=analyses,
                         metrics=system_metrics)


@app.route('/api/trigger-alert', methods=['POST'])
def trigger_alert():
    """Simulate alert trigger"""
    alert_data = request.json
    return jsonify({
        'success': True,
        'alert_id': f"ALT-{int(time.time())}",
        'message': 'Alert processed successfully',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting DYNAMIC Support Insight Analyzer")
    print("📍 Live application at: http://localhost:5000")
    print("📊 Real-time data generation: ACTIVE")
    print("🤖 AI Analysis Engine: READY")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)