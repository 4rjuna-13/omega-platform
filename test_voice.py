#!/usr/bin/env python3
"""Simple voice test"""

print("=== VOICE SYSTEM TEST ===\n")

# Test 1: Check PyAudio
print("1. Testing PyAudio...")
try:
    import pyaudio
    p = pyaudio.PyAudio()
    print(f"   ✅ PyAudio {pyaudio.__version__} installed")
    
    # List audio devices
    print("   Audio devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"     {i}: {info['name']} (inputs: {info['maxInputChannels']})")
    p.terminate()
    
except ImportError:
    print("   ❌ PyAudio not installed")
    print("   Run: pip install pyaudio")
except Exception as e:
    print(f"   ⚠️  PyAudio error: {e}")

print("\n2. Testing SpeechRecognition...")
try:
    import speech_recognition as sr
    print(f"   ✅ SpeechRecognition {sr.__version__} installed")
    
    # List microphones
    print("   Available microphones:")
    mics = sr.Microphone.list_microphone_names()
    for i, mic in enumerate(mics[:5]):  # Show first 5
        print(f"     {i}: {mic}")
    if len(mics) > 5:
        print(f"     ... and {len(mics) - 5} more")
        
except ImportError:
    print("   ❌ SpeechRecognition not installed")
except Exception as e:
    print(f"   ⚠️  SpeechRecognition error: {e}")

print("\n3. Testing Text-to-Speech...")
try:
    import pyttsx3
    print("   ✅ pyttsx3 installed")
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"   Available voices: {len(voices)}")
    for voice in voices[:3]:  # Show first 3 voices
        print(f"     - {voice.name}")
    
except ImportError:
    print("   ❌ pyttsx3 not installed")
except Exception as e:
    print(f"   ⚠️  pyttsx3 error: {e}")

print("\n4. Testing voice_module...")
try:
    from voice_module import VoiceCommandProcessor
    vcp = VoiceCommandProcessor()
    status = vcp.get_status()
    
    print("   Voice module status:")
    for key, value in status.items():
        print(f"     {key}: {'✅' if value else '❌'}")
        
except Exception as e:
    print(f"   ⚠️  Voice module error: {e}")

print("\n=== TEST COMPLETE ===")
