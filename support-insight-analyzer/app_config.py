import os
from datetime import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    DEBUG = True
    
    # System Configuration
    SYSTEM_NAME = "SUPPORT INSIGHT ANALYZER - ENTERPRISE AI AGENT"
    SYSTEM_VERSION = "2.0.0"
    
    # Paths
    UPLOAD_FOLDER = 'uploads'
    ANALYSIS_FOLDER = 'analysis_results'
    
    # Agent Settings
    MAX_AGENTS = 5
    ANALYSIS_TIMEOUT = 300  # 5 minutes
    
    def __init__(self):
        self.initialize_directories()
    
    def initialize_directories(self):
        os.makedirs(self.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(self.ANALYSIS_FOLDER, exist_ok=True)

config = Config()