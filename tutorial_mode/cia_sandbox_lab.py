#!/usr/bin/env python3
"""
CIA Triad Sandbox Lab - Hands-on practice environment.
"""
import os
import tempfile
import hashlib
from datetime import datetime
from loguru import logger

# Import your platform's modules
try:
    from enhanced_crypto import encrypt_data, decrypt_data
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    logger.warning("enhanced_crypto.py not available - using simulated crypto")

class CIASandboxLab:
    """Interactive sandbox to practice CIA triad principles."""
    
    def __init__(self):
        self.workspace = tempfile.mkdtemp(prefix="cia_lab_")
        self.artifacts = []
        logger.info(f"CIA Sandbox Lab initialized at: {self.workspace}")
    
    def confidentiality_exercise(self):
        """Practice encryption/decryption."""
        print("\n🔒 **CONFIDENTIALITY EXERCISE**")
        print("Create and protect a secret message.")
        
        secret_message = input("Enter a secret message to protect: ").strip()
        if not secret_message:
            secret_message = "Default secret: JAIDA protects the triad!"
        
        # Simulate encryption
        secret_file = os.path.join(self.workspace, "secret_message.enc")
        
        if CRYPTO_AVAILABLE:
            encrypted = encrypt_data(secret_message, key="cia_lab_demo")
            with open(secret_file, 'w') as f:
                f.write(encrypted)
        else:
            # Simulated encryption (base64)
            import base64
            encoded = base64.b64encode(secret_message.encode()).decode()
            with open(secret_file, 'w') as f:
                f.write(f"ENCRYPTED:{encoded}")
        
        self.artifacts.append(secret_file)
        print(f"✅ Message encrypted and saved to: {secret_file}")
        
        # Challenge: Can they decrypt it?
        print("\n🔓 **DECRYPTION CHALLENGE**")
        print("The encrypted message is:")
        with open(secret_file, 'r') as f:
            print(f"   {f.read()[:50]}...")
        
        if input("\nTry to decrypt? (y/n): ").lower() == 'y':
            if CRYPTO_AVAILABLE:
                with open(secret_file, 'r') as f:
                    decrypted = decrypt_data(f.read(), key="cia_lab_demo")
                print(f"✅ Decrypted: {decrypted}")
            else:
                print("⚠️  Real encryption/decryption requires enhanced_crypto.py")
        
        return True
    
    def integrity_exercise(self):
        """Practice file integrity verification."""
        print("\n📊 **INTEGRITY EXERCISE**")
        print("Detect if a file has been tampered with.")
        
        # Create a document
        doc_content = f"""SECURITY LOG - {datetime.now()}
System: Omega Platform
Status: Secure
CIA Triad Status: All principles enforced
Threat Level: Low
"""
        doc_file = os.path.join(self.workspace, "security_log.txt")
        with open(doc_file, 'w') as f:
            f.write(doc_content)
        
        # Calculate original hash
        with open(doc_file, 'rb') as f:
            original_hash = hashlib.sha256(f.read()).hexdigest()
        
        print(f"✅ Created document: {doc_file}")
        print(f"📝 Original SHA-256 hash: {original_hash[:16]}...")
        
        # Tamper with the file
        print("\n⚡ **SIMULATING TAMPERING**")
        time.sleep(1)
        
        with open(doc_file, 'a') as f:
            f.write("\n[UNAUTHORIZED MODIFICATION: Threat Level changed to CRITICAL]")
        
        print("⚠️  File has been modified by an attacker!")
        
        # Challenge: Detect the tampering
        print("\n🔍 **DETECTION CHALLENGE**")
        print("Calculate the new hash and compare:")
        
        with open(doc_file, 'rb') as f:
            new_hash = hashlib.sha256(f.read()).hexdigest()
        
        print(f"   New SHA-256 hash: {new_hash[:16]}...")
        print(f"   Hashes match? {'❌ NO - INTEGRITY BREACH!' if original_hash != new_hash else '✅ YES'}")
        
        self.artifacts.append(doc_file)
        return True
    
    def availability_exercise(self):
        """Practice availability monitoring."""
        print("\n🌐 **AVAILABILITY EXERCISE**")
        print("Monitor critical service status.")
        
        services_to_check = ["python3", "systemd", "network"]
        print(f"Checking services: {', '.join(services_to_check)}")
        
        available_count = 0
        for service in services_to_check:
            # Simulate service check
            if service in ["python3", "systemd"]:
                status = "✅ RUNNING"
                available_count += 1
            else:
                status = "⚠️  DEGRADED"
            
            print(f"   {service}: {status}")
        
        print(f"\n📈 Availability Score: {available_count}/{len(services_to_check)}")
        
        if available_count < len(services_to_check):
            print("\n🚨 **RESPONSE CHALLENGE**")
            print("A service is degraded! What would you do?")
            print("1. Check logs (/var/log/)")
            print("2. Restart the service")
            print("3. Failover to backup")
            
            response = input("\nYour choice (1-3): ").strip()
            if response in ['1', '2', '3']:
                print(f"✅ Good choice! Option {response} is appropriate.")
            else:
                print("⚠️  In crisis, any action is better than none!")
        
        return True
    
    def run_lab(self):
        """Execute the complete sandbox lab."""
        print("\n" + "="*60)
        print("🛠️  CIA TRIAD SANDBOX LAB")
        print("="*60)
        print(f"Workspace: {self.workspace}")
        print("Complete all 3 exercises to master the CIA Triad.\n")
        
        exercises = [
            ("Confidentiality", self.confidentiality_exercise),
            ("Integrity", self.integrity_exercise),
            ("Availability", self.availability_exercise)
        ]
        
        completed = 0
        for name, exercise_func in exercises:
            try:
                if exercise_func():
                    completed += 1
                    print(f"\n✅ {name} exercise completed!")
                time.sleep(1)
            except Exception as e:
                print(f"❌ {name} exercise failed: {e}")
        
        print("\n" + "="*60)
        print(f"🏆 LAB COMPLETE: {completed}/3 exercises finished")
        print(f"📁 Artifacts created in: {self.workspace}")
        print("="*60)
        
        # Cleanup prompt
        if input("\nClean up workspace? (y/n): ").lower() == 'y':
            import shutil
            shutil.rmtree(self.workspace)
            print("✅ Workspace cleaned up.")
        else:
            print(f"⚠️  Workspace preserved at: {self.workspace}")
        
        return completed

# One-liner test
if __name__ == "__main__":
    print("[*] Starting CIA Triad Sandbox Lab...")
    lab = CIASandboxLab()
    lab.run_lab()
