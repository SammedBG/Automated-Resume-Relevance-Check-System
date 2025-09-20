"""
Configuration settings for Resume Relevance Check System
"""

import os
from typing import Dict, Any

class Config:
    """Configuration class with default settings"""
    
    # API Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_BATCH_SIZE: int = 50
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///resume_analysis.db"
    
    # Processing Configuration
    HARD_MATCH_WEIGHT: float = 0.6
    SEMANTIC_MATCH_WEIGHT: float = 0.4
    VERDICT_THRESHOLDS: Dict[str, float] = {
        "high": 0.6,
        "medium": 0.35,
        "low": 0.0
    }
    
    # Security Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # File Processing
    SUPPORTED_EXTENSIONS: list = ['.pdf', '.docx', '.txt']
    MAX_TEXT_LENGTH: int = 100000  # 100KB of text
    
    # NLP Configuration
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # Performance Configuration
    CACHE_TTL: int = 3600  # 1 hour
    MAX_CONCURRENT_JOBS: int = 5
    
    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """Get all configuration settings as dictionary"""
        return {
            'openai_api_key': cls.OPENAI_API_KEY,
            'max_file_size': cls.MAX_FILE_SIZE,
            'max_batch_size': cls.MAX_BATCH_SIZE,
            'database_url': cls.DATABASE_URL,
            'hard_match_weight': cls.HARD_MATCH_WEIGHT,
            'semantic_match_weight': cls.SEMANTIC_MATCH_WEIGHT,
            'verdict_thresholds': cls.VERDICT_THRESHOLDS,
            'secret_key': cls.SECRET_KEY,
            'access_token_expire_minutes': cls.ACCESS_TOKEN_EXPIRE_MINUTES,
            'supported_extensions': cls.SUPPORTED_EXTENSIONS,
            'max_text_length': cls.MAX_TEXT_LENGTH,
            'spacy_model': cls.SPACY_MODEL,
            'sentence_transformer_model': cls.SENTENCE_TRANSFORMER_MODEL,
            'cache_ttl': cls.CACHE_TTL,
            'max_concurrent_jobs': cls.MAX_CONCURRENT_JOBS
        }

# Create global config instance
config = Config()
