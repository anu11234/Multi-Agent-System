import logging
from datetime import datetime
from .analysis_agent import AnalysisAgent

class Orchestrator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.analysis_agent = AnalysisAgent()
        self.logger = logging.getLogger('orchestrator')
        self.system_status = "Ready"
    
    def run_complete_analysis(self):
        """Run complete multi-agent pipeline analysis"""
        self.logger.info("🚀 Starting multi-agent analysis pipeline...")
        
        try:
            # Step 1: Data Collection
            self.logger.info("📊 Step 1: Collecting recent tickets...")
            recent_tickets = self.memory_manager.get_recent_tickets(days=7)
            
            if not recent_tickets:
                return {"error": "No recent tickets found for analysis"}
            
            # Step 2: Sentiment Analysis
            self.logger.info("😊 Step 2: Analyzing customer sentiment...")
            sentiment_analysis = self.analysis_agent.analyze_sentiment(recent_tickets)
            
            # Step 3: Trend Detection
            self.logger.info("📈 Step 3: Detecting emerging trends...")
            trend_analysis = self.analysis_agent.detect_trends(recent_tickets)
            
            # Step 4: Priority Analysis
            self.logger.info("🎯 Step 4: Analyzing ticket priorities...")
            priority_analysis = self.analysis_agent.analyze_priorities(recent_tickets)
            
            # Step 5: Generate Insights
            self.logger.info("💡 Step 5: Generating insights...")
            insights = self.analysis_agent.generate_insights(
                sentiment_analysis, 
                trend_analysis, 
                priority_analysis
            )
            
            # Compile final results
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "tickets_analyzed": len(recent_tickets),
                "time_period": "7 days",
                "sentiment_analysis": sentiment_analysis,
                "trend_analysis": trend_analysis,
                "priority_analysis": priority_analysis,
                "key_insights": insights,
                "recommendations": self.analysis_agent.generate_recommendations(insights)
            }
            
            # Save analysis
            analysis_id = self.memory_manager.save_analysis(analysis_results)
            analysis_results['analysis_id'] = analysis_id
            
            self.logger.info("✅ Multi-agent analysis completed successfully!")
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"❌ Analysis failed: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def get_system_status(self):
        """Get current system status"""
        stats = self.memory_manager.get_ticket_statistics()
        
        return {
            "system_status": self.system_status,
            "environment": "configured successfully",
            "genini_agent": "Ready",
            "local_memory": "Ready",
            "multi_agent_system": "Ready",
            "statistics": stats,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }