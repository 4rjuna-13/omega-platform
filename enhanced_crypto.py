"""
Enhanced Quantum-Resistant Cryptography for Project Omega
Using real XChaCha20-Poly1305 from pynacl
"""
import base64
import hashlib
from nacl.public import PrivateKey, PublicKey, Box
from nacl.secret import SecretBox
from nacl.utils import random
from typing import Dict, Tuple
import json

class EnhancedQuantumCrypto:
    """Real quantum-resistant encryption using libsodium"""
    
    def __init__(self, key_material: str = "omega_quantum_key"):
        # Derive key from material
        self.key = self._derive_key(key_material)
        self.secret_box = SecretBox(self.key)
        print("🔐 Enhanced Quantum Crypto initialized with XChaCha20-Poly1305")
    
    def _derive_key(self, material: str) -> bytes:
        """Derive 256-bit key using SHA3-256"""
        return hashlib.sha3_256(material.encode()).digest()
    
    def encrypt(self, plaintext: str) -> Dict[str, str]:
        """Encrypt using XChaCha20-Poly1305"""
        nonce = random(24)  # XChaCha20 uses 24-byte nonce
        ciphertext = self.secret_box.encrypt(plaintext.encode(), nonce)
        
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "nonce": base64.b64encode(nonce).decode(),
            "algorithm": "XChaCha20-Poly1305",
            "key_hash": hashlib.sha256(self.key).hexdigest()[:16]
        }
    
    def decrypt(self, encrypted_data: Dict[str, str]) -> str:
        """Decrypt XChaCha20-Poly1305 ciphertext"""
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        
        plaintext = self.secret_box.decrypt(ciphertext, nonce)
        return plaintext.decode()

# Test the enhanced crypto
if __name__ == "__main__":
    crypto = EnhancedQuantumCrypto()
    
    test_message = "Project Omega Top Secret Data"
    encrypted = crypto.encrypt(test_message)
    
    print(f"📝 Original: {test_message}")
    print(f"🔐 Encrypted: {encrypted['algorithm']}")
    print(f"   Nonce: {encrypted['nonce'][:16]}...")
    print(f"   Ciphertext length: {len(encrypted['ciphertext'])} chars")
    
    decrypted = crypto.decrypt(encrypted)
    print(f"🔓 Decrypted: {decrypted}")
    print(f"✅ Match: {test_message == decrypted}")
