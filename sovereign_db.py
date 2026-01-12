#!/usr/bin/env python3
"""
SOVEREIGN_DB: Persistent Data Layer - FIXED VERSION
"""
import json
import sqlite3
import threading
from datetime import datetime
from typing import Dict, List, Any
import hashlib

class SovereignDB:
    def __init__(self, db_path: str = "sovereign_data.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_database()
        
    def _init_database(self):
        """Initialize database without hanging"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simplified schema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                bot_id TEXT PRIMARY KEY,
                bot_class TEXT,
                bot_type TEXT,
                capabilities TEXT,
                status TEXT,
                created_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threats (
                threat_id TEXT PRIMARY KEY,
                ioc_type TEXT,
                ioc_value TEXT,
                source_layer TEXT,
                confidence REAL,
                first_seen TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
        
    def register_bot(self, bot_id: str, bot_class: str, bot_type: str, capabilities: List[str]) -> bool:
        """Simple bot registration without deadlock"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO bots 
            (bot_id, bot_class, bot_type, capabilities, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            bot_id, bot_class, bot_type, 
            json.dumps(capabilities), "ACTIVE", datetime.now()
        ))
        
        conn.commit()
        conn.close()
        return True
        
    def store_ioc(self, ioc_type: str, ioc_value: str, source_layer: str, confidence: float = 0.5) -> str:
        """Simple IOC storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        threat_id = f"THREAT-{hashlib.md5(f'{ioc_type}:{ioc_value}'.encode()).hexdigest()[:8]}"
        
        cursor.execute('''
            INSERT OR REPLACE INTO threats 
            (threat_id, ioc_type, ioc_value, source_layer, confidence, first_seen)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            threat_id, ioc_type, ioc_value, source_layer, confidence, datetime.now()
        ))
        
        conn.commit()
        conn.close()
        return threat_id
        
    def get_metrics(self):
        """Get basic metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM bots")
        bot_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM threats")
        threat_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "bots": {"total": bot_count},
            "threats": {"total": threat_count},
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print("🧪 Testing Fixed SovereignDB...")
    db = SovereignDB()
    
    # Quick test
    db.register_bot("TEST-BOT-001", "WD", "test", ["test"])
    db.store_ioc("test", "test.com", "test", 0.8)
    
    metrics = db.get_metrics()
    print(f"✅ Test complete: {metrics['bots']['total']} bots, {metrics['threats']['total']} threats")
