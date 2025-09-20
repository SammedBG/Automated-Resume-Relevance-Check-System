import pandas as pd
import json
from typing import List, Dict
import csv
import io

def export_results(results: List[Dict], format: str = 'csv') -> str:
    """Export results to CSV or JSON format"""
    
    if format.lower() == 'csv':
        return export_to_csv(results)
    elif format.lower() == 'json':
        return export_to_json(results)
    else:
        raise ValueError("Format must be 'csv' or 'json'")

def export_to_csv(results: List[Dict]) -> str:
    """Export results to CSV format"""
    if not results:
        return ""
    
    # Flatten the results for CSV export
    flattened_results = []
    for result in results:
        flat_result = {
            'filename': result.get('filename', ''),
            'score': result.get('score', 0),
            'verdict': result.get('verdict', ''),
            'hard_match_score': result.get('hard_match_score', 0),
            'semantic_score': result.get('semantic_score', 0),
            'missing_skills': ', '.join(result.get('missing_skills', [])),
            'suggestions': result.get('suggestions', ''),
            'processed_at': result.get('processed_at', ''),
            'created_at': result.get('created_at', '')
        }
        flattened_results.append(flat_result)
    
    # Convert to CSV
    df = pd.DataFrame(flattened_results)
    return df.to_csv(index=False)

def export_to_json(results: List[Dict]) -> str:
    """Export results to JSON format"""
    return json.dumps(results, indent=2, default=str)

def calculate_metrics(results: List[Dict]) -> Dict:
    """Calculate summary metrics from results"""
    if not results:
        return {
            'total_resumes': 0,
            'average_score': 0,
            'high_suitability': 0,
            'medium_suitability': 0,
            'low_suitability': 0,
            'high_percentage': 0,
            'medium_percentage': 0,
            'low_percentage': 0
        }
    
    total = len(results)
    scores = [r.get('score', 0) for r in results]
    verdicts = [r.get('verdict', 'Low') for r in results]
    
    high_count = verdicts.count('High')
    medium_count = verdicts.count('Medium')
    low_count = verdicts.count('Low')
    
    return {
        'total_resumes': total,
        'average_score': sum(scores) / total if scores else 0,
        'high_suitability': high_count,
        'medium_suitability': medium_count,
        'low_suitability': low_count,
        'high_percentage': (high_count / total) * 100 if total > 0 else 0,
        'medium_percentage': (medium_count / total) * 100 if total > 0 else 0,
        'low_percentage': (low_count / total) * 100 if total > 0 else 0
    }

def format_suggestions(suggestions: str) -> str:
    """Format suggestions for better display"""
    if not suggestions:
        return "No specific suggestions available."
    
    # Split by newlines and format as bullet points
    lines = suggestions.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line:
            if not line.startswith('•') and not line.startswith('-'):
                line = f"• {line}"
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def validate_file_type(filename: str) -> bool:
    """Validate if file type is supported"""
    supported_extensions = ['.pdf', '.docx', '.txt']
    return any(filename.lower().endswith(ext) for ext in supported_extensions)

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    import re
    # Remove or replace invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized[:255]  # Limit length

def get_file_size_mb(file) -> float:
    """Get file size in MB"""
    file.seek(0, 2)  # Seek to end
    size = file.tell()
    file.seek(0)  # Reset to beginning
    return size / (1024 * 1024)

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def format_score(score: float) -> str:
    """Format score for display"""
    return f"{score:.1%}" if score <= 1.0 else f"{score:.2f}"

def get_verdict_color(verdict: str) -> str:
    """Get color code for verdict display"""
    colors = {
        'High': '#28a745',    # Green
        'Medium': '#ffc107',  # Yellow
        'Low': '#dc3545'      # Red
    }
    return colors.get(verdict, '#6c757d')  # Default gray

def create_summary_report(results: List[Dict]) -> str:
    """Create a text summary report"""
    if not results:
        return "No results to summarize."
    
    metrics = calculate_metrics(results)
    
    report = f"""
RESUME ANALYSIS SUMMARY REPORT
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW:
- Total Resumes Processed: {metrics['total_resumes']}
- Average Score: {metrics['average_score']:.2f}

SUITABILITY BREAKDOWN:
- High Suitability: {metrics['high_suitability']} ({metrics['high_percentage']:.1f}%)
- Medium Suitability: {metrics['medium_suitability']} ({metrics['medium_percentage']:.1f}%)
- Low Suitability: {metrics['low_suitability']} ({metrics['low_percentage']:.1f}%)

TOP PERFORMERS:
"""
    
    # Sort by score and get top 5
    sorted_results = sorted(results, key=lambda x: x.get('score', 0), reverse=True)
    for i, result in enumerate(sorted_results[:5], 1):
        report += f"{i}. {result.get('filename', 'Unknown')} - Score: {result.get('score', 0):.2f} ({result.get('verdict', 'Unknown')})\n"
    
    return report