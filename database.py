import sqlite3
import json
from datetime import datetime
from typing import Dict, List
import os

class DatabaseManager:
    def __init__(self, db_path: str = "resume_analysis.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                score REAL NOT NULL,
                verdict TEXT NOT NULL,
                hard_match_score REAL,
                semantic_score REAL,
                missing_skills TEXT,
                suggestions TEXT,
                processed_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create job_descriptions table for audit
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_result(self, result: Dict):
        """Save analysis result to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO results (
                filename, score, verdict, hard_match_score, semantic_score,
                missing_skills, suggestions, processed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['filename'],
            result.get('final_score', result.get('score', 0)),
            result['verdict'],
            result.get('hard_match_score', 0),
            result.get('semantic_score', 0),
            json.dumps(result.get('missing_skills', [])),
            result.get('suggestions', ''),
            result.get('processed_at', '')
        ))
        
        conn.commit()
        conn.close()
        
        # Also save to JSON for backup
        self.save_to_json(result)
    
    def save_to_json(self, result: Dict):
        """Save result to JSON file for backup"""
        json_file = "results_backup.json"
        
        # Load existing results
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                results = json.load(f)
        else:
            results = []
        
        # Add new result
        results.append(result)
        
        # Save back to file
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def get_all_results(self) -> List[Dict]:
        """Retrieve all results from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, score, verdict, hard_match_score, semantic_score,
                   missing_skills, suggestions, processed_at, created_at
            FROM results
            ORDER BY created_at DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            result = {
                'filename': row[0],
                'score': row[1],
                'verdict': row[2],
                'hard_match_score': row[3],
                'semantic_score': row[4],
                'missing_skills': json.loads(row[5]) if row[5] else [],
                'suggestions': row[6],
                'processed_at': row[7],
                'created_at': row[8]
            }
            results.append(result)
        
        return results
    
    def get_results_by_verdict(self, verdict: str) -> List[Dict]:
        """Get results filtered by verdict"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT filename, score, verdict, hard_match_score, semantic_score,
                   missing_skills, suggestions, processed_at, created_at
            FROM results
            WHERE verdict = ?
            ORDER BY score DESC
        ''', (verdict,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = []
        for row in rows:
            result = {
                'filename': row[0],
                'score': row[1],
                'verdict': row[2],
                'hard_match_score': row[3],
                'semantic_score': row[4],
                'missing_skills': json.loads(row[5]) if row[5] else [],
                'suggestions': row[6],
                'processed_at': row[7],
                'created_at': row[8]
            }
            results.append(result)
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get summary statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM results')
        total_count = cursor.fetchone()[0]
        
        # Average score
        cursor.execute('SELECT AVG(score) FROM results')
        avg_score = cursor.fetchone()[0] or 0
        
        # Verdict distribution
        cursor.execute('SELECT verdict, COUNT(*) FROM results GROUP BY verdict')
        verdict_dist = dict(cursor.fetchall())
        
        # Recent activity (last 7 days)
        cursor.execute('''
            SELECT COUNT(*) FROM results 
            WHERE created_at >= datetime('now', '-7 days')
        ''')
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_processed': total_count,
            'average_score': round(avg_score, 3),
            'verdict_distribution': verdict_dist,
            'recent_activity': recent_count
        }
    
    def clear_all_results(self):
        """Clear all results (for testing/reset)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM results')
        cursor.execute('DELETE FROM job_descriptions')
        
        conn.commit()
        conn.close()
        
        # Also clear JSON backup
        if os.path.exists("results_backup.json"):
            os.remove("results_backup.json")