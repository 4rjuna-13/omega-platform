#!/usr/bin/env python3
"""
Check what unified_orchestrator.py does
"""
import subprocess
import sys

print("🔍 Checking unified_orchestrator.py...")

# Try to run it with different commands
commands = ["status", "autonomous", "deploy", "demo"]

for cmd in commands:
    print(f"\nTrying command: {cmd}")
    try:
        result = subprocess.run(
            [sys.executable, "unified_orchestrator.py", cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout[:200]}...")
        if result.stderr:
            print(f"Error: {result.stderr[:200]}...")
    except subprocess.TimeoutExpired:
        print("⏱️  Command timed out (likely running in background)")
    except Exception as e:
        print(f"❌ Error: {e}")
