#!/usr/bin/env python3
"""
JAIDA LLM Analyst - Real AI integration for OTX pipeline
This replaces the simulation with local Ollama AI
"""

import json
import logging
from typing import Dict, Any
import sys
import subprocess

# Add simple_jaida to path
sys.path.append('.')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('jaida')

class JAIDALLMAnalyst:
    """
    Main analyst class used by otx_llm_pipeline_fixed.py
    Now with REAL AI using Ollama qwen2.5:0.5b
    """
    
    def __init__(self):
        self.model = "qwen2.5:0.5b"
        logger.info(f"Initialized JAIDALLMAnalyst with model: {self.model}")
    
    def analyze_threat_intel(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main analysis method - called by OTX pipeline
        Replaces simulation with real AI analysis
        """
        logger.info(f"Analyzing threat: {threat_data.get('name', 'unknown')[:50]}...")
        
        # Prepare prompt for the AI
        prompt = self._create_prompt(threat_data)
        
        try:
            # Call Ollama
            result = subprocess.run(
                ['ollama', 'run', self.model, prompt],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            if result.returncode != 0:
                logger.error(f"Ollama error: {result.stderr[:200]}")
                return self._fallback_analysis(threat_data)
            
            response = result.stdout.strip()
            logger.debug(f"AI raw response: {response[:200]}...")
            
            # Parse the response
            analysis = self._parse_ai_response(response, threat_data)
            
            # Ensure CIA scores are in 0-10 range (AI sometimes returns 0-100)
            analysis = self._normalize_cia_scores(analysis)
            
            logger.info(f"✅ Analysis complete: {analysis.get('classification', 'unknown')}")
            return analysis
            
        except subprocess.TimeoutExpired:
            logger.error("AI analysis timeout")
            return self._fallback_analysis(threat_data, "timeout")
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return self._fallback_analysis(threat_data, str(e))
    
    def _create_prompt(self, threat_data: Dict[str, Any]) -> str:
        """Create optimized prompt for threat analysis"""
        # Extract key information
        name = threat_data.get('name', 'Unknown threat')
        description = threat_data.get('description', 'No description')
        tags = threat_data.get('tags', [])
        indicators = [threat_data.get(k, '') for k in ['indicator', 'hostname', 'domain'] if k in threat_data]
        
        prompt = f"""As JAIDA (Autonomous Cyber Threat Intelligence System), analyze this threat.

THREAT: {name}
DESCRIPTION: {description}
TAGS: {', '.join(tags) if tags else 'None'}
INDICATORS: {', '.join(filter(None, indicators)) if indicators else 'None'}

Return ONLY a JSON object with these exact keys:
{{
  "cia_triad_impact": {{
    "confidentiality": <0-10>,
    "integrity": <0-10>,
    "availability": <0-10>
  }},
  "classification": "<malware/phishing/apt/exploit/ddos/suspicious/benign>",
  "recommended_action": "<specific action string>",
  "confidence": <0.0-1.0>,
  "analysis_summary": "<brief summary>"
}}

Ensure all numbers are between 0-10, not 0-100."""
        
        return prompt
    
    def _parse_ai_response(self, response: str, original_threat: Dict) -> Dict[str, Any]:
        """Parse AI response into structured analysis"""
        # Clean response
        response = response.strip()
        
        # Find JSON in response
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start == -1 or end == -1:
            logger.warning("No JSON found in AI response")
            return self._extract_from_text(response, original_threat)
        
        json_str = response[start:end]
        
        try:
            data = json.loads(json_str)
            
            # Convert to expected format (cia_triad_impact -> cia_scores)
            if 'cia_triad_impact' in data:
                data['cia_scores'] = data.pop('cia_triad_impact')
            elif 'cia_scores' not in data:
                data['cia_scores'] = {"confidentiality": 5, "integrity": 5, "availability": 5}
            
            # Ensure all required fields
            required = {
                'classification': 'unknown',
                'recommended_action': 'investigate',
                'confidence': 0.5,
                'analysis_summary': 'AI analysis completed'
            }
            
            for key, default in required.items():
                if key not in data:
                    data[key] = default
            
            return data
            
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            return self._extract_from_text(response, original_threat)
    
    def _extract_from_text(self, text: str, threat: Dict) -> Dict[str, Any]:
        """Extract analysis from free text when JSON parsing fails"""
        text_lower = text.lower()
        
        # Determine classification
        classification = "suspicious"
        scores = {"confidentiality": 5, "integrity": 5, "availability": 5}
        
        # Check for keywords
        if any(kw in text_lower for kw in ['malware', 'virus', 'trojan', 'ransomware']):
            classification = "malware"
            scores = {"confidentiality": 8, "integrity": 9, "availability": 7}
        elif any(kw in text_lower for kw in ['phish', 'credential', 'login', 'password']):
            classification = "phishing"
            scores = {"confidentiality": 9, "integrity": 6, "availability": 4}
        elif any(kw in text_lower for kw in ['apt', 'advanced persistent']):
            classification = "apt"
            scores = {"confidentiality": 9, "integrity": 9, "availability": 8}
        elif any(kw in text_lower for kw in ['exploit', 'vulnerability', 'cve']):
            classification = "exploit"
            scores = {"confidentiality": 7, "integrity": 8, "availability": 6}
        elif any(kw in text_lower for kw in ['ddos', 'denial of service']):
            classification = "ddos"
            scores = {"confidentiality": 3, "integrity": 4, "availability": 9}
        
        # Extract confidence hints
        confidence = 0.5
        if 'high confidence' in text_lower or 'confident' in text_lower:
            confidence = 0.8
        elif 'medium' in text_lower:
            confidence = 0.6
        elif 'low' in text_lower:
            confidence = 0.3
        
        return {
            "cia_scores": scores,
            "classification": classification,
            "recommended_action": "Further investigation required",
            "confidence": confidence,
            "analysis_summary": text[:150] + "..."
        }
    
    def _normalize_cia_scores(self, analysis: Dict) -> Dict:
        """Ensure CIA scores are in 0-10 range (not 0-100)"""
        if 'cia_scores' in analysis:
            for key in ['confidentiality', 'integrity', 'availability']:
                if key in analysis['cia_scores']:
                    score = analysis['cia_scores'][key]
                    # If score > 10, assume it's 0-100 scale and convert
                    if isinstance(score, (int, float)) and score > 10:
                        analysis['cia_scores'][key] = min(10, max(0, score / 10))
                    elif not isinstance(score, (int, float)):
                        analysis['cia_scores'][key] = 5
        return analysis
    
    def _fallback_analysis(self, threat_data: Dict, reason: str = "unknown") -> Dict[str, Any]:
        """Fallback when AI fails"""
        logger.warning(f"Using fallback analysis: {reason}")
        
        # Simple heuristic based on threat name/description
        threat_text = str(threat_data).lower()
        
        if any(kw in threat_text for kw in ['phish', 'login', 'credential']):
            scores = {"confidentiality": 8, "integrity": 5, "availability": 3}
            classification = "phishing"
        elif any(kw in threat_text for kw in ['malware', 'ransomware', 'trojan']):
            scores = {"confidentiality": 7, "integrity": 8, "availability": 6}
            classification = "malware"
        elif any(kw in threat_text for kw in ['ddos', 'flood', 'botnet']):
            scores = {"confidentiality": 3, "integrity": 4, "availability": 9}
            classification = "ddos"
        else:
            scores = {"confidentiality": 5, "integrity": 5, "availability": 5}
            classification = "suspicious"
        
        return {
            "cia_scores": scores,
            "classification": classification,
            "recommended_action": f"Review manually (AI failed: {reason})",
            "confidence": 0.1,
            "analysis_summary": f"Fallback analysis: {reason}"
        }
    
    def generate_lesson_from_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate training lesson from analysis
        Called by OTX pipeline
        """
        classification = analysis.get('classification', 'unknown')
        cia_scores = analysis.get('cia_scores', {})
        
        # Map classification to lesson type
        lesson_map = {
            'phishing': 'Phishing Defense Lab',
            'malware': 'Malware Analysis Workshop',
            'apt': 'Advanced Threat Hunting',
            'exploit': 'Vulnerability Management',
            'ddos': 'DDoS Mitigation Strategies',
            'suspicious': 'Threat Investigation Basics'
        }
        
        lesson_type = lesson_map.get(classification, 'General Cybersecurity Lab')
        
        # Determine difficulty based on CIA scores
        avg_score = sum(cia_scores.values()) / 3 if cia_scores else 5
        if avg_score >= 8:
            difficulty = "Advanced"
        elif avg_score >= 5:
            difficulty = "Intermediate"
        else:
            difficulty = "Beginner"
        
        return {
            "title": f"{lesson_type} - {difficulty}",
            "description": f"Hands-on lab for {classification} threats based on recent intelligence",
            "difficulty": difficulty,
            "estimated_time": "60 minutes",
            "learning_objectives": [
                f"Identify {classification} indicators",
                "Apply appropriate mitigation techniques",
                "Analyze threat intelligence reports"
            ],
            "prerequisites": ["Basic cybersecurity knowledge"],
            "classification": classification,
            "cia_scores": cia_scores
        }

# For backward compatibility
def simulate_llm_analysis(threat_data):
    """Legacy function - now uses real AI"""
    analyst = JAIDALLMAnalyst()
    return analyst.analyze_threat_intel(threat_data)

# Test
if __name__ == "__main__":
    print("🧪 Testing JAIDALLMAnalyst with real AI...")
    analyst = JAIDALLMAnalyst()
    
    test_threat = {
        "name": "Test phishing campaign",
        "description": "Fake banking website stealing credentials",
        "tags": ["phishing", "financial"],
        "indicator": "secure-bank-login.com"
    }
    
    result = analyst.analyze_threat_intel(test_threat)
    print("Analysis result:")
    print(json.dumps(result, indent=2))
    
    lesson = analyst.generate_lesson_from_analysis(result)
    print("\nGenerated lesson:")
    print(json.dumps(lesson, indent=2))
