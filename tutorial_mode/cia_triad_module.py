#!/usr/bin/env python3
"""
CIA Triad Lesson Module - Interactive learning with theory and examples.
"""
from loguru import logger
import time

class CIATriadLesson:
    """Interactive lesson on Confidentiality, Integrity, Availability."""
    
    def __init__(self, user_level=1):
        self.user_level = user_level
        self.completed = False
        self.score = 0
        logger.info(f"CIA Triad Lesson initialized for level {user_level}")
    
    def present_theory(self):
        """Core theory presentation - adaptive based on user level."""
        theory_content = {
            1: """📚 **CIA TRIAD - SECURITY FUNDAMENTALS**
                
The CIA Triad is the foundation of ALL cybersecurity:
1. **Confidentiality** = Keeping secrets secret
   • Example: Passwords, encryption, access controls
   
2. **Integrity** = Trusting your data is accurate
   • Example: File hashes, digital signatures
   
3. **Availability** = Having access when you need it
   • Example: Backups, DDoS protection, redundancy""",
            
            2: """🎯 **CIA TRIAD - PRACTICAL APPLICATION**
                
Real-world implementations:
• **Confidentiality**: AES-256 encryption in your enhanced_crypto.py
• **Integrity**: SHA-256 hashes to verify file integrity
• **Availability**: Load balancers and failover systems in SAIOS""",
            
            3: """🚀 **CIA TRIAD - ADVANCED IMPLICATIONS**
                
Trade-offs and conflicts:
• Strong encryption (Confidentiality) can slow systems (Availability)
• Complex integrity checks impact performance
• Balancing all three requires architectural planning"""
        }
        
        # Adaptive content: higher level gets more advanced theory
        content = theory_content.get(min(self.user_level, 3), theory_content[1])
        print(f"\n{content}\n")
        return content
    
    def interactive_examples(self):
        """Let the user identify CIA principles in scenarios."""
        scenarios = [
            {
                "scenario": "A hospital database encrypts patient records.",
                "correct": "confidentiality",
                "explanation": "✅ Correct! Encryption protects patient privacy (Confidentiality)."
            },
            {
                "scenario": "A banking system uses checksums to detect altered transactions.",
                "correct": "integrity", 
                "explanation": "✅ Correct! Checksums verify data hasn't been tampered with (Integrity)."
            },
            {
                "scenario": "A website uses multiple servers so it stays online during attacks.",
                "correct": "availability",
                "explanation": "✅ Correct! Redundant servers maintain access (Availability)."
            }
        ]
        
        print("\n🔍 **IDENTIFY THE CIA PRINCIPLE**")
        print("For each scenario, type: confidentiality, integrity, or availability\n")
        
        for i, scenario in enumerate(scenarios[:self.user_level + 1], 1):
            print(f"{i}. {scenario['scenario']}")
            user_answer = input("Your answer: ").strip().lower()
            
            if user_answer == scenario['correct']:
                print(f"   {scenario['explanation']}")
                self.score += 1
            else:
                print(f"   ⚠️  Actually, this demonstrates {scenario['correct'].title()}.")
                print(f"   {scenario['explanation'][2:]}")
            
            time.sleep(0.5)
        
        return self.score
    
    def code_connection(self):
        """Show how CIA triad is implemented in YOUR Omega platform."""
        print("\n💻 **CIA IN YOUR OMEGA PLATFORM**")
        
        code_examples = {
            "Confidentiality": "enhanced_crypto.py - Implements AES-256 encryption",
            "Integrity": "sovereign_data.db - Uses SQLite transactions for data consistency",
            "Availability": "unified_orchestrator.py - Main service that must stay running"
        }
        
        for principle, example in code_examples.items():
            print(f"• {principle}: {example}")
        
        # One-liner to demonstrate file integrity check
        print("\n🔐 **TRY THIS INTEGRITY CHECK:**")
        print('''import hashlib
with open("unified_orchestrator.py", "rb") as f:
    print(f"SHA-256: {hashlib.sha256(f.read()).hexdigest()[:16]}...")''')
    
    def run_lesson(self):
        """Execute the complete lesson."""
        print("\n" + "="*60)
        print("🔐 LESSON: CIA SECURITY TRIAD")
        print("="*60)
        
        self.present_theory()
        self.interactive_examples()
        self.code_connection()
        
        self.completed = True
        print(f"\n📊 Lesson complete! Score: {self.score}/{(self.user_level + 1)}")
        print("="*60)
        
        return {
            "module": "cia_triad",
            "completed": self.completed,
            "score": self.score,
            "max_score": (self.user_level + 1)
        }

# One-liner to test the lesson
if __name__ == "__main__":
    print("[*] Testing CIA Triad Lesson Module...")
    lesson = CIATriadLesson(user_level=2)
    lesson.run_lesson()
