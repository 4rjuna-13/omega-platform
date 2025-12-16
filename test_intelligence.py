#!/usr/bin/env python3
"""Omega Intelligence Test"""

print("=== OMEGA INTELLIGENCE TEST ===")

# Test imports
tests = [
    ("numpy", lambda: __import__("numpy")),
    ("scikit-learn", lambda: __import__("sklearn")),
    ("predictive_threat", lambda: __import__("predictive_threat")),
    ("voice_module", lambda: __import__("voice_module")),
]

print("\nTesting imports:")
for name, import_func in tests:
    try:
        import_func()
        print(f"  ✅ {name}")
    except ImportError as e:
        print(f"  ❌ {name}: {e}")

# Test predictive threat model
print("\nTesting threat predictor:")
try:
    from predictive_threat import ThreatPredictor
    predictor = ThreatPredictor()
    print("  ✅ ThreatPredictor instantiated")
    
    # Quick test
    test_data = {'ports': [80, 443, 22], 'auth_attempts': {'ssh': 2}}
    features = predictor.extract_features(test_data)
    print(f"  ✅ Feature extraction: {len(features)} features")
    
except Exception as e:
    print(f"  ❌ Threat predictor test failed: {e}")

print("\n=== TEST COMPLETE ===")
print("Ready for Omega Intelligence!")
