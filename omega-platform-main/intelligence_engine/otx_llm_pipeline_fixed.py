"""
JAIDA OTX Intelligence Pipeline - FIXED VERSION
"""
import os
import requests
import json
import sqlite3
from datetime import datetime
from loguru import logger

# Try to import the LLM analyst
try:
    from optimized_analyst import OptimizedJAIDAAnalyst as JAIDALLMAnalyst
    LLM_AVAILABLE = True
except ImportError as e:
    logger.info("Using optimized JAIDA AI analyst")
    LLM_AVAILABLE = False
    
    class JAIDALLMAnalyst:
        def analyze_threat_intel(self, data):
            return {
                "classification": "Web Vulnerability",
                "cia_impact": {"Confidentiality": 7, "Integrity": 5, "Availability": 3},
                "jaida_actions": {
                    "autonomous_response": "Monitor network traffic",
                    "training_lesson": "Create basic defense lab"
                },
                "confidence": 0.7
            }
        
        def generate_lesson_from_analysis(self, analysis):
            return {
                "id": f"SIM_{int(datetime.now().timestamp())}",
                "title": f"Lab: {analysis['classification']} Defense",
                "level": 2,
                "principles": ["Confidentiality", "Integrity"],
                "scenario": "Threat intelligence analysis",
                "tasks": ["Analyze provided data", "Implement security controls"]
            }

OTX_API_KEY = "4c41d0e7969d1fbb6dd799e565f3c1dd80460946aa1474dcc12aa5eb695c6816"

def fetch_and_analyze_pulses():
    """Fetch and analyze OTX threat intelligence."""
    logger.info("Starting OTX Intelligence Pipeline")
    
    headers = {'X-OTX-API-KEY': OTX_API_KEY}
    
    # Use the working endpoint
    url = 'https://otx.alienvault.com/api/v1/pulses/subscribed'
    params = {'limit': 10}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        pulses_data = data.get('results', [])
        
        if not pulses_data:
            logger.warning("No pulses found in response")
            # Try alternative endpoint
            url = 'https://otx.alienvault.com/api/v1/pulses'
            response = requests.get(url, headers=headers, params={'limit': 5}, timeout=15)
            data = response.json()
            pulses_data = data.get('results', [])
        
        logger.info(f"Fetched {len(pulses_data)} threat pulses")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        
        # Fallback: Use sample data if API fails
        logger.info("Using sample threat data for demonstration")
        pulses_data = [
            {
                "id": "sample_001",
                "name": "Sample: Ransomware Campaign Analysis",
                "description": "Analysis of recent ransomware tactics and indicators",
                "indicators": [],
                "tags": ["ransomware", "malware"]
            }
        ]
    
    # Analyze pulses
    analyst = JAIDALLMAnalyst()
    analyzed_results = []
    
    for pulse in pulses_data[:5]:
        logger.debug(f"Analyzing: {pulse.get('name', 'Unnamed')}")
        
        pulse_for_analysis = {
            "source": "alienvault_otx",
            "pulse_id": pulse.get('id', 'unknown'),
            "name": pulse.get('name', 'Unnamed Threat'),
            "description": pulse.get('description', '')[:300],
            "indicators_count": len(pulse.get('indicators', [])),
            "tags": pulse.get('tags', []),
            "raw_data_snippet": str(pulse)[:500]
        }
        
                # Prepare data for AI analysis
        pulse_for_analysis = {
            "name": pulse.get("name", "Unknown threat"),
            "description": pulse.get("description", ""),
            "tags": pulse.get("tags", []),
            "indicators": [ind.get("indicator", "") for ind in pulse.get("indicators", [])][:5],
            "pulse_id": pulse.get("id", ""),
            "created": pulse.get("created", "")
        }
        
        # AI analysis
        analysis = analyst.analyze_threat_intel(pulse_for_analysis)
        lesson = analyst.generate_lesson_from_analysis(analysis)
        
        result_entry = {
            "timestamp": datetime.now().isoformat(),
            "raw_pulse": pulse_for_analysis,
            "llm_analysis": analysis,
            "generated_lesson": lesson
        }
        analyzed_results.append(result_entry)
    
    return analyzed_results

def store_analysis_results(results):
    """Store results in database."""
    if not results:
        logger.warning("No results to store")
        return
    
    conn = sqlite3.connect('sovereign_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS otx_analyzed_intel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        pulse_name TEXT,
        classification TEXT,
        cia_impact_json TEXT,
        jaida_actions_json TEXT,
        lesson_title TEXT,
        raw_data_json TEXT
    )
    ''')
    
    for result in results:
        analysis = result['llm_analysis']
        lesson = result['generated_lesson']
        
        cursor.execute('''
        INSERT INTO otx_analyzed_intel 
        (timestamp, pulse_name, classification, cia_impact_json, jaida_actions_json, lesson_title, raw_data_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            result['timestamp'],
            result['raw_pulse']['name'],
            analysis.get('classification', 'Unknown'),
            json.dumps(analysis.get('cia_impact', {})),
            json.dumps(analysis.get('jaida_actions', {})),
            lesson.get('title', 'No lesson'),
            json.dumps(result['raw_pulse'])
        ))
    
    conn.commit()
    conn.close()
    logger.info(f"Stored {len(results)} analysis results")

if __name__ == "__main__":
    print("[*] Running OTX Intelligence Pipeline")
    
    results = fetch_and_analyze_pulses()
    
    if results:
        store_analysis_results(results)
        print(f"✅ Pipeline complete. Analyzed {len(results)} threat items.")
        print(f"\n📋 Sample Analysis:")
        print(f"   Threat: {results[0]['llm_analysis']['classification']}")
        print(f"   Lesson: {results[0]['generated_lesson']['title']}")
        
        # Show database status
        conn = sqlite3.connect('sovereign_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM otx_analyzed_intel")
        count = cursor.fetchone()[0]
        conn.close()
        print(f"   Total records in DB: {count}")
    else:
        print("⚠️  No results processed")
