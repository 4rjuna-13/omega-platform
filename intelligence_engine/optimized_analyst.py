#!/usr/bin/env python3
"""
Optimized JAIDA Analyst with faster prompts and better reliability
"""

import subprocess, json, logging, sqlite3, time
from datetime import datetime

logging.basicConfig(level=logging.WARNING)  # Reduce logging noise
logger = logging.getLogger('jaida')

class OptimizedJAIDAAnalyst:
    def __init__(self):
        self.model = "qwen2.5:0.5b"
        self.timeout = 60  # 60 second timeout
        logger.info(f"Optimized analyst using {self.model}")
    
    def analyze_threat_intel(self, threat_data):
        """Optimized analysis with faster prompt"""
        # Extract minimal info for prompt
        name = threat_data.get('name', 'Threat')[:50]
        desc = threat_data.get('description', '')[:100]
        
        # Ultra-fast prompt
        prompt = f"""Analyze threat: {name}. Brief: {desc}. 
        Return JSON: {{"classification":"type","cia_scores":{{"c":0-10,"i":0-10,"a":0-10}},"confidence":0.0-1.0}}"""
        
        try:
            start = time.time()
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            elapsed = time.time() - start
            
            if result.returncode != 0:
                logger.warning(f"Ollama error, using fast fallback")
                return self._fast_fallback(threat_data)
            
            text = result.stdout
            logger.debug(f"Analysis took {elapsed:.1f}s")
            
            # Try to parse
            try:
                start_idx = text.find('{')
                end_idx = text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    data = json.loads(text[start_idx:end_idx])
                    # Normalize keys
                    if 'cia_scores' in data:
                        if 'c' in data['cia_scores']:
                            data['cia_scores']['confidentiality'] = data['cia_scores'].pop('c')
                        if 'i' in data['cia_scores']:
                            data['cia_scores']['integrity'] = data['cia_scores'].pop('i')
                        if 'a' in data['cia_scores']:
                            data['cia_scores']['availability'] = data['cia_scores'].pop('a')
                    return data
            except:
                pass
            
            # If parsing failed, use keyword detection
            return self._extract_from_keywords(text, threat_data)
            
        except subprocess.TimeoutExpired:
            logger.warning(f"Timeout after {self.timeout}s, using fallback")
            return self._fast_fallback(threat_data)
        except Exception as e:
            logger.warning(f"Error: {e}, using fallback")
            return self._fast_fallback(threat_data)
    
    def _extract_from_keywords(self, text, threat_data):
        """Fast keyword extraction"""
        text_lower = text.lower()
        threat_lower = str(threat_data).lower()
        
        # Classification
        if 'phish' in text_lower or 'phish' in threat_lower:
            cls = "phishing"
            scores = {"confidentiality": 8, "integrity": 5, "availability": 3}
        elif 'malware' in text_lower or 'ransom' in text_lower or 'virus' in text_lower:
            cls = "malware"
            scores = {"confidentiality": 7, "integrity": 8, "availability": 6}
        elif 'ddos' in text_lower or 'dos' in text_lower:
            cls = "ddos"
            scores = {"confidentiality": 3, "integrity": 4, "availability": 9}
        elif 'exploit' in text_lower or 'cve' in text_lower:
            cls = "exploit"
            scores = {"confidentiality": 6, "integrity": 7, "availability": 5}
        else:
            cls = "suspicious"
            scores = {"confidentiality": 5, "integrity": 5, "availability": 5}
        
        # Confidence from keywords
        conf = 0.5
        if 'high' in text_lower:
            conf = 0.8
        elif 'medium' in text_lower:
            conf = 0.6
        
        return {
            "cia_scores": scores,
            "classification": cls,
            "confidence": conf,
            "recommended_action": "investigate",
            "analysis_summary": "AI analysis completed"
        }
    
    def _fast_fallback(self, threat_data):
        """Ultra-fast fallback analysis"""
        text = str(threat_data).lower()
        
        if 'phish' in text:
            scores = {"confidentiality": 8, "integrity": 5, "availability": 3}
            cls = "phishing"
        elif 'malware' in text or 'ransom' in text:
            scores = {"confidentiality": 7, "integrity": 8, "availability": 6}
            cls = "malware"
        elif 'ddos' in text:
            scores = {"confidentiality": 3, "integrity": 4, "availability": 9}
            cls = "ddos"
        else:
            scores = {"confidentiality": 5, "integrity": 5, "availability": 5}
            cls = "suspicious"
        
        return {
            "cia_scores": scores,
            "classification": cls,
            "confidence": 0.3,
            "recommended_action": "review_manually",
            "analysis_summary": "Fast fallback analysis"
        }
    
    def generate_lesson_from_analysis(self, analysis):
        """Simple lesson generation"""
        cls = analysis.get('classification', 'unknown')
        return {
            "title": f"{cls.title()} Defense Lab",
            "description": f"Hands-on training for {cls} threats",
            "difficulty": "Intermediate",
            "estimated_time": "60 minutes"
        }

# Test
if __name__ == "__main__":
    analyst = OptimizedJAIDAAnalyst()
    test = {"name": "Test phishing", "description": "Phishing test"}
    print("Testing optimized analyst...")
    result = analyst.analyze_threat_intel(test)
    print(json.dumps(result, indent=2))
