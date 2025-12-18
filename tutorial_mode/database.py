#!/usr/bin/env python3
"""
JAIDA Tutorial Database - Manages user progress and learning content in sovereign_data.db
"""
import sqlite3
import os
from loguru import logger

class TutorialDatabase:
    """Manages all tutorial-related data in the sovereign database."""
    
    def __init__(self, db_path="sovereign_data.db"):
        self.db_path = db_path
        self.init_database()
        logger.info(f"Tutorial database connected: {db_path}")
    
    def init_database(self):
        """Initialize tutorial tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tutorial-specific tables
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutorial_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            skill_level INTEGER DEFAULT 1,
            current_module TEXT,
            progress_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutorial_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            topic TEXT,
            difficulty INTEGER DEFAULT 1,
            correct_answer TEXT,
            explanation TEXT,
            module_name TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutorial_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            module_name TEXT,
            score REAL,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES tutorial_users (user_id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_user_progress(self, user_id, skill_level, current_module, progress_data):
        """Save or update user progress - the essential one-liner for persistence."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Upsert user progress
        cursor.execute('''
        INSERT INTO tutorial_users (user_id, skill_level, current_module, progress_json, last_active)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            skill_level = excluded.skill_level,
            current_module = excluded.current_module,
            progress_json = excluded.progress_json,
            last_active = CURRENT_TIMESTAMP
        ''', (user_id, skill_level, current_module, str(progress_data)))
        
        conn.commit()
        conn.close()
        return True
    
    def load_questions(self, difficulty_max=3, topic=None):
        """Load questions from database - adaptive learning core."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM tutorial_questions WHERE difficulty <= ?"
        params = [difficulty_max]
        
        if topic:
            query += " AND topic = ?"
            params.append(topic)
        
        query += " ORDER BY RANDOM() LIMIT 5"
        
        cursor.execute(query, params)
        questions = cursor.fetchall()
        conn.close()
        
        return questions
    
    def seed_sample_questions(self):
        """Seed the database with sample questions if empty."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if we have questions
        cursor.execute("SELECT COUNT(*) FROM tutorial_questions")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_questions = [
                ("What is a DDoS attack?", "basic", 1, 
                 "Distributed Denial of Service - overwhelming a target with traffic",
                 "DDoS attacks use multiple systems to flood a target, making it unavailable to users.",
                 "Network Fundamentals"),
                ("Explain symmetric vs asymmetric encryption.", "crypto", 2,
                 "Symmetric uses one key, asymmetric uses public/private key pair",
                 "Symmetric is faster for bulk data, asymmetric enables secure key exchange.",
                 "Cryptography Basics"),
                ("What is the CIA triad in cybersecurity?", "concepts", 1,
                 "Confidentiality, Integrity, Availability",
                 "The foundational model for security policies: keeping data secret, accurate, and accessible.",
                 "Security Fundamentals"),
                ("How does a firewall work?", "network", 2,
                 "Filters network traffic based on predefined security rules",
                 "Firewalls act as barriers between trusted and untrusted networks, inspecting packets.",
                 "Network Defense"),
                ("What is SQL injection?", "web", 3,
                 "Injecting malicious SQL code through user inputs",
                 "Attackers exploit vulnerable input fields to manipulate database queries.",
                 "Web Security")
            ]
            
            cursor.executemany('''
            INSERT INTO tutorial_questions (question, topic, difficulty, correct_answer, explanation, module_name)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_questions)
            
            logger.info(f"Seeded {len(sample_questions)} sample questions")
        
        conn.commit()
        conn.close()

# One-liner utility function
def get_tutorial_db():
    """Factory function to get tutorial database instance."""
    return TutorialDatabase()

if __name__ == "__main__":
    # Test the database
    db = TutorialDatabase()
    db.seed_sample_questions()
    print(f"✅ Tutorial database initialized at: {db.db_path}")
    questions = db.load_questions(difficulty_max=2)
    print(f"📚 Loaded {len(questions)} questions for difficulty <= 2")
