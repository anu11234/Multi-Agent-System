import pandas as pd
from textblob import TextBlob
from collections import Counter
import logging
from datetime import datetime, timedelta

class AnalysisAgent:
    def __init__(self):
        self.logger = logging.getLogger('analysis_agent')
    
    def analyze_sentiment(self, tickets):
        """Analyze sentiment from ticket descriptions"""
        sentiments = []
        sentiment_scores = []
        
        for ticket in tickets:
            # Simple sentiment analysis using TextBlob
            description = f"{ticket['subject']} {ticket['description']}"
            blob = TextBlob(description)
            sentiment_score = blob.sentiment.polarity
            
            if sentiment_score > 0.1:
                sentiment = "Positive"
            elif sentiment_score < -0.1:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            
            sentiments.append(sentiment)
            sentiment_scores.append(sentiment_score)
        
        sentiment_distribution = Counter(sentiments)
        avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return {
            "distribution": dict(sentiment_distribution),
            "average_score": round(avg_sentiment_score, 3),
            "total_positive": sentiment_distribution.get("Positive", 0),
            "total_negative": sentiment_distribution.get("Negative", 0),
            "total_neutral": sentiment_distribution.get("Neutral", 0)
        }
    
    def detect_trends(self, tickets):
        """Detect emerging trends and patterns"""
        df = pd.DataFrame(tickets)
        
        # Trend analysis by category
        category_trends = df['category'].value_counts().to_dict()
        
        # Priority trends
        priority_trends = df['priority'].value_counts().to_dict()
        
        # Daily ticket volume
        daily_volume = df['created_date'].value_counts().sort_index().to_dict()
        
        # Emerging issues (categories with increasing frequency)
        emerging_categories = []
        for category, count in category_trends.items():
            if count >= 3:  # Threshold for emerging trend
                emerging_categories.append({
                    "category": category,
                    "frequency": count,
                    "trend": "Increasing" if count > 5 else "Stable"
                })
        
        return {
            "category_trends": category_trends,
            "priority_trends": priority_trends,
            "daily_volume": daily_volume,
            "emerging_issues": sorted(emerging_categories, key=lambda x: x['frequency'], reverse=True),
            "most_common_category": max(category_trends.items(), key=lambda x: x[1])[0] if category_trends else "N/A"
        }
    
    def analyze_priorities(self, tickets):
        """Analyze ticket priorities and urgency"""
        df = pd.DataFrame(tickets)
        
        priority_stats = {
            "Critical": len(df[df['priority'] == 'Critical']),
            "High": len(df[df['priority'] == 'High']),
            "Medium": len(df[df['priority'] == 'Medium']),
            "Low": len(df[df['priority'] == 'Low'])
        }
        
        # Priority by category
        priority_by_category = {}
        for category in df['category'].unique():
            category_data = df[df['category'] == category]
            priority_by_category[category] = category_data['priority'].value_counts().to_dict()
        
        urgency_score = (
            priority_stats['Critical'] * 4 + 
            priority_stats['High'] * 3 + 
            priority_stats['Medium'] * 2 + 
            priority_stats['Low'] * 1
        ) / len(tickets) if tickets else 0
        
        return {
            "priority_distribution": priority_stats,
            "priority_by_category": priority_by_category,
            "urgency_score": round(urgency_score, 2),
            "requires_immediate_attention": priority_stats['Critical'] + priority_stats['High']
        }
    
    def generate_insights(self, sentiment_analysis, trend_analysis, priority_analysis):
        """Generate actionable insights from analysis results"""
        insights = []
        
        # Sentiment insights
        if sentiment_analysis['total_negative'] > sentiment_analysis['total_positive']:
            insights.append({
                "type": "warning",
                "title": "High Negative Sentiment",
                "description": f"Negative sentiment ({sentiment_analysis['total_negative']} tickets) exceeds positive sentiment. Consider proactive outreach.",
                "priority": "High"
            })
        
        # Priority insights
        if priority_analysis['requires_immediate_attention'] > 5:
            insights.append({
                "type": "critical",
                "title": "High Priority Backlog",
                "description": f"{priority_analysis['requires_immediate_attention']} tickets require immediate attention.",
                "priority": "Critical"
            })
        
        # Trend insights
        emerging_issues = trend_analysis['emerging_issues']
        if emerging_issues and emerging_issues[0]['frequency'] > 8:
            insights.append({
                "type": "info",
                "title": "Emerging Issue Detected",
                "description": f"'{emerging_issues[0]['category']}' shows increasing frequency ({emerging_issues[0]['frequency']} cases).",
                "priority": "Medium"
            })
        
        # Performance insights
        total_tickets = sum(trend_analysis['category_trends'].values())
        if total_tickets > 50:
            insights.append({
                "type": "success",
                "title": "High Ticket Volume",
                "description": f"Analyzed {total_tickets} tickets in the period. Consider scaling support resources.",
                "priority": "Medium"
            })
        
        return sorted(insights, key=lambda x: {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}[x['priority']])
    
    def generate_recommendations(self, insights):
        """Generate recommendations based on insights"""
        recommendations = []
        
        for insight in insights:
            if insight['type'] == 'critical':
                recommendations.append({
                    "action": "Immediate Review Required",
                    "description": f"Address {insight['title']} as top priority",
                    "timeline": "Within 24 hours"
                })
            elif insight['type'] == 'warning':
                recommendations.append({
                    "action": "Sentiment Improvement",
                    "description": "Implement customer satisfaction measures",
                    "timeline": "Within 1 week"
                })
        
        # Add general recommendations
        recommendations.extend([
            {
                "action": "Weekly Trend Review",
                "description": "Schedule regular analysis of emerging trends",
                "timeline": "Ongoing"
            },
            {
                "action": "Agent Training",
                "description": "Focus training on most common issue categories",
                "timeline": "Next month"
            }
        ])
        
        return recommendations