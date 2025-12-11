import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
from config import Config

class DatabaseManager:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Create and return a database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize the database with schema."""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema = f.read()
        
        conn = self.get_connection()
        try:
            conn.executescript(schema)
            conn.commit()
        finally:
            conn.close()
    
    # User operations
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """Create a new user and return the user ID."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        conn = self.get_connection()
        try:
            cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        conn = self.get_connection()
        try:
            cursor = conn.execute('SELECT * FROM users WHERE email = ?', (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        conn = self.get_connection()
        try:
            cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    # Interview operations
    def create_interview(self, user_id: int, cv_filename: Optional[str],
                        cv_analysis: Optional[str], question_count: int,
                        difficulty_level: str) -> int:
        """Create a new interview and return the interview ID."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO interviews 
                   (user_id, cv_filename, cv_analysis, question_count, difficulty_level)
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, cv_filename, cv_analysis, question_count, difficulty_level)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def get_interview(self, interview_id: int) -> Optional[Dict[str, Any]]:
        """Get interview by ID."""
        conn = self.get_connection()
        try:
            cursor = conn.execute('SELECT * FROM interviews WHERE id = ?', (interview_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def get_user_interviews(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all interviews for a user."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                'SELECT * FROM interviews WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def update_interview_status(self, interview_id: int, status: str,
                               score: Optional[float] = None):
        """Update interview status and optionally score."""
        conn = self.get_connection()
        try:
            if status == 'completed':
                conn.execute(
                    '''UPDATE interviews 
                       SET status = ?, score = ?, completed_at = CURRENT_TIMESTAMP
                       WHERE id = ?''',
                    (status, score, interview_id)
                )
            else:
                conn.execute(
                    'UPDATE interviews SET status = ?, score = ? WHERE id = ?',
                    (status, score, interview_id)
                )
            conn.commit()
        finally:
            conn.close()
    
    # Question operations
    def add_question(self, interview_id: int, question_text: str,
                    question_order: int) -> int:
        """Add a question to an interview."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO questions (interview_id, question_text, question_order)
                   VALUES (?, ?, ?)''',
                (interview_id, question_text, question_order)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def update_question_answer(self, question_id: int, answer_text: str):
        """Update the answer for a question."""
        conn = self.get_connection()
        try:
            conn.execute(
                'UPDATE questions SET answer_text = ? WHERE id = ?',
                (answer_text, question_id)
            )
            conn.commit()
        finally:
            conn.close()
    
    def get_interview_questions(self, interview_id: int) -> List[Dict[str, Any]]:
        """Get all questions for an interview."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                'SELECT * FROM questions WHERE interview_id = ? ORDER BY question_order',
                (interview_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()
    
    # Evaluation operations
    def create_evaluation(self, interview_id: int, evaluation_text: str,
                         score: float, feedback: str) -> int:
        """Create an evaluation for an interview."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                '''INSERT INTO evaluations 
                   (interview_id, evaluation_text, score, feedback)
                   VALUES (?, ?, ?, ?)''',
                (interview_id, evaluation_text, score, feedback)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def get_interview_evaluation(self, interview_id: int) -> Optional[Dict[str, Any]]:
        """Get evaluation for an interview."""
        conn = self.get_connection()
        try:
            cursor = conn.execute(
                'SELECT * FROM evaluations WHERE interview_id = ? ORDER BY created_at DESC LIMIT 1',
                (interview_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()