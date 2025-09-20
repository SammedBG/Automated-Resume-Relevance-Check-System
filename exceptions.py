"""
Custom exceptions for Resume Relevance Check System
"""

class ResumeAnalysisError(Exception):
    """Base exception for resume analysis errors"""
    pass

class ModelLoadingError(ResumeAnalysisError):
    """Raised when a model fails to load"""
    def __init__(self, model_name: str, error_message: str):
        self.model_name = model_name
        self.error_message = error_message
        super().__init__(f"Failed to load {model_name}: {error_message}")

class ScoringError(ResumeAnalysisError):
    """Raised when scoring calculation fails"""
    def __init__(self, scoring_type: str, error_message: str):
        self.scoring_type = scoring_type
        self.error_message = error_message
        super().__init__(f"Scoring error in {scoring_type}: {error_message}")

class FileProcessingError(ResumeAnalysisError):
    """Raised when file processing fails"""
    def __init__(self, filename: str, error_message: str):
        self.filename = filename
        self.error_message = error_message
        super().__init__(f"File processing error for {filename}: {error_message}")

class DatabaseError(ResumeAnalysisError):
    """Raised when database operations fail"""
    def __init__(self, operation: str, error_message: str):
        self.operation = operation
        self.error_message = error_message
        super().__init__(f"Database error during {operation}: {error_message}")

class ValidationError(ResumeAnalysisError):
    """Raised when input validation fails"""
    def __init__(self, field: str, error_message: str):
        self.field = field
        self.error_message = error_message
        super().__init__(f"Validation error for {field}: {error_message}")

class APIError(ResumeAnalysisError):
    """Raised when external API calls fail"""
    def __init__(self, api_name: str, error_message: str):
        self.api_name = api_name
        self.error_message = error_message
        super().__init__(f"API error for {api_name}: {error_message}")
