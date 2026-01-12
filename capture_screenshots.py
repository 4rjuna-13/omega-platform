"""
Generate demo screenshots for marketing
"""
print("\n" + "="*60)
print("📸 GENERATING LAUNCH ASSETS")
print("="*60)

screenshots = [
    ("welcome.png", "▶️  Step 1: Welcome to Project Omega"),
    ("sandbox.png", "🔒 ENABLING SAFE SANDBOX MODE"),
    ("detect.png", "▶️  Step 3: Detect Your First Attack"),
    ("complete.png", "🎉 FIRST 15 MINUTES COMPLETE!"),
    ("metrics.png", "📊 MARKETING METRICS UPDATED:")
]

print("\n🎨 Screenshots needed for launch:")
for filename, caption in screenshots:
    print(f"  📸 {filename:20} - {caption[:40]}...")

print("\n" + "="*60)
print("🎬 VIDEO SCRIPT (30 seconds)")
print("="*60)
print("""
[0-5s] - Show welcome screen: "Launch Your Cybersecurity Career"
[5-15s] - Show sandbox activation: "Zero-risk learning"
[15-25s] - Show attack detection: "Hands-on experience"
[25-30s] - Show completion: "Your first 15 minutes done!"
""")

print("\n" + "="*60)
print("📝 LAUNCH POST TEMPLATES")
print("="*60)
print("""
**Hacker News Title:** Show HN: Project Omega - Open-source security training platform
**Key point:** First 15 minutes gets you from zero to detecting/deceiving attacks

**GitHub:** "Getting Started: python3 omega_v4_phase_2g_final.py"
**Reddit r/cybersecurity:** "Finally: A free, open-source alternative to..."
""")
