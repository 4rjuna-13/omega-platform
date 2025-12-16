#!/usr/bin/env python3
print("🚀 PROJECT OMEGA - FINAL LAUNCH VERIFICATION")
print("=" * 60)

import os
import sys

print("Checking core files...")

# Check main file
if os.path.exists("omega_v4_phase_2g_final.py"):
    print("✅ omega_v4_phase_2g_final.py")
else:
    print("❌ omega_v4_phase_2g_final.py")

# Check tutorial system
if os.path.exists("tutorial_system"):
    print("✅ tutorial_system/ directory")
else:
    print("❌ tutorial_system/ directory")

# Check README
if os.path.exists("README.md"):
    print("✅ README.md")
else:
    print("❌ README.md - creating minimal one")
    with open("README.md", "w") as f:
        f.write("# Project Omega\nSecurity training platform")

print("\n✅ Basic verification complete!")
