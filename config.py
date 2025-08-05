import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

class Config:
    # Gmail settings
    GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
    
    # AI settings  
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Application settings
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 300))  # 5 dakika varsayılan
    MAX_EMAILS_PER_CHECK = int(os.getenv('MAX_EMAILS_PER_CHECK', 5))  # Daha az e-posta
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Security settings
    MAX_RESPONSE_ATTEMPTS = int(os.getenv('MAX_RESPONSE_ATTEMPTS', 3))
    RATE_LIMIT_DELAY = int(os.getenv('RATE_LIMIT_DELAY', 2))
    
    # Gmail API settings
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send'
    ]
    
    CREDENTIALS_FILE = 'credentials/credentials.json'
    TOKEN_FILE = 'token.json'
    
    @classmethod
    def validate(cls):
        """Validate required configuration with detailed error messages"""
        required_vars = {
            'GMAIL_ADDRESS': cls.GMAIL_ADDRESS,
            'GEMINI_API_KEY': cls.GEMINI_API_KEY
        }
        
        missing = []
        invalid = []
        
        for var, value in required_vars.items():
            if not value:
                missing.append(var)
            elif var == 'GMAIL_ADDRESS' and '@' not in value:
                invalid.append(f"{var}: Invalid email format")
            elif var == 'GEMINI_API_KEY' and (len(value) < 20 or not value.startswith('AIza')):
                invalid.append(f"{var}: Invalid API key format")
        
        # Check file existence
        if not Path(cls.CREDENTIALS_FILE).exists():
            missing.append(f"Credentials file: {cls.CREDENTIALS_FILE}")
        
        if missing:
            raise ValueError(f"Missing required configuration: {', '.join(missing)}")
        
        if invalid:
            raise ValueError(f"Invalid configuration: {', '.join(invalid)}")
        
        return True
    
    @classmethod
    def get_safe_config(cls):
        """Return configuration without sensitive data for logging"""
        return {
            'gmail_address': cls.GMAIL_ADDRESS,
            'check_interval': cls.CHECK_INTERVAL,
            'max_emails': cls.MAX_EMAILS_PER_CHECK,
            'log_level': cls.LOG_LEVEL
        }