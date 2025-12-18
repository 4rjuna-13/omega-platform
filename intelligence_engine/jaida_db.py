#!/usr/bin/env python3
"""
JAIDA Database Helper - Uses Python's sqlite3 module instead of broken CLI
"""

import sqlite3
import json
from datetime import datetime

def query_database(query, params=None):
    """Execute SQL query using Python's sqlite3 module"""
    try:
        conn = sqlite3.connect('../sovereign_data.db')
        conn.row_factory = sqlite3.Row  # Return dictionaries
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        # Fetch results
        if query.strip().upper().startswith('SELECT'):
            results = [dict(row) for row in cursor.fetchall()]
        else:
            conn.commit()
            results = cursor.rowcount
            
        conn.close()
        return {"success": True, "data": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

def get_recent_analyses(limit=5):
    """Get recent AI analyses"""
    return query_database(
        "SELECT timestamp, threat_indicator, classification, "
        "cia_confidentiality, cia_integrity, cia_availability, confidence "
        "FROM jaida_analyses ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )

def get_analysis_stats():
    """Get analysis statistics"""
    return query_database('''
        SELECT 
            COUNT(*) as total_analyses,
            COUNT(DISTINCT classification) as unique_classes,
            AVG(confidence) as avg_confidence,
            AVG(cia_confidentiality) as avg_confidentiality,
            AVG(cia_integrity) as avg_integrity,
            AVG(cia_availability) as avg_availability
        FROM jaida_analyses
    ''')

# Command-line interface
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "recent":
            result = get_recent_analyses(3)
            if result["success"]:
                print("Recent AI analyses:")
                for row in result["data"]:
                    print(f"  {row['timestamp'][:16]} | {row['threat_indicator'][:30]:30} | "
                          f"{row['classification']:15} | conf: {row['confidence']:.2f}")
            else:
                print(f"Error: {result['error']}")
        elif sys.argv[1] == "stats":
            result = get_analysis_stats()
            if result["success"] and result["data"]:
                stats = result["data"][0]
                print("Database Statistics:")
                print(f"  Total analyses: {stats['total_analyses']}")
                print(f"  Unique threat types: {stats['unique_classes']}")
                print(f"  Avg confidence: {stats['avg_confidence']:.2f}")
                print(f"  Avg CIA: C={stats['avg_confidentiality']:.1f}, "
                      f"I={stats['avg_integrity']:.1f}, A={stats['avg_availability']:.1f}")
        else:
            # Direct query
            result = query_database(" ".join(sys.argv[1:]))
            if result["success"]:
                if isinstance(result["data"], list) and result["data"]:
                    print(json.dumps(result["data"], indent=2))
                else:
                    print(f"Query executed: {result['data']} rows affected")
            else:
                print(f"Error: {result['error']}")
    else:
        print("JAIDA Database Helper")
        print("Usage:")
        print("  python3 jaida_db.py recent          # Show recent analyses")
        print("  python3 jaida_db.py stats           # Show statistics")
        print("  python3 jaida_db.py 'SQL QUERY'     # Execute custom query")
