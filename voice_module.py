import sys
import time

class VoiceCommandProcessor:
    """Hands-free Omega control with fallback options"""
    
    def __init__(self):
        self.recognizer = None
        self.engine = None
        self.microphone_available = False
        self.tts_available = False
        
        # Try to initialize speech recognition
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            
            # Check for PyAudio
            try:
                import pyaudio
                self.microphone_available = True
                print("[VOICE] Microphone access available")
            except ImportError:
                print("[VOICE] PyAudio not installed - microphone disabled")
                print("[VOICE] Install with: pip install pyaudio")
                
        except ImportError:
            print("[VOICE] SpeechRecognition not available")
        
        # Try to initialize text-to-speech
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.tts_available = True
            print("[VOICE] Text-to-speech available")
        except Exception as e:
            print(f"[VOICE] Text-to-speech error: {e}")
            print("[VOICE] Install eSpeak: sudo apt-get install espeak espeak-ng")
        
    def listen_command(self, timeout=5, phrase_time_limit=10):
        """Capture voice input and convert to text"""
        if not self.recognizer or not self.microphone_available:
            return "[VOICE] Microphone not available"
        
        try:
            import speech_recognition as sr
            
            # Use default microphone
            with sr.Microphone() as source:
                print(f"[VOICE] Listening for {timeout} seconds... (speak now)")
                
                # Adjust for ambient noise - shorter duration
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    # Listen with timeout
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit
                    )
                    
                    # Recognize using Google Web Speech API
                    command = self.recognizer.recognize_google(audio)
                    print(f"[VOICE] Heard: {command}")
                    return command
                    
                except sr.WaitTimeoutError:
                    return "[VOICE] Listening timed out - no speech detected"
                except sr.UnknownValueError:
                    return "[VOICE] Could not understand audio"
                except sr.RequestError as e:
                    return f"[VOICE] Speech service error: {e}"
                except Exception as e:
                    return f"[VOICE] Error: {str(e)}"
                    
        except Exception as e:
            return f"[VOICE] Microphone error: {str(e)}"
    
    def speak(self, text):
        """Text-to-speech output"""
        if not self.engine or not self.tts_available:
            print(f"[VOICE TTS] (Simulated): {text}")
            return False
        
        try:
            print(f"[VOICE] Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"[VOICE TTS Error]: {e}")
            return False
    
    def get_status(self):
        """Get voice module status"""
        return {
            "microphone": self.microphone_available,
            "text_to_speech": self.tts_available,
            "speech_recognition": self.recognizer is not None
        }

# Alternative: Fallback voice processor for testing
class SimulatedVoiceProcessor:
    """Simulated voice for testing without hardware"""
    
    def __init__(self):
        print("[VOICE SIM] Using simulated voice processor")
    
    def listen_command(self, timeout=5, phrase_time_limit=10):
        """Simulate voice input with text input"""
        try:
            command = input("[VOICE SIM] Enter command (simulating voice input): ")
            return command
        except:
            return "[VOICE SIM] No input received"
    
    def speak(self, text):
        """Simulate speech output"""
        print(f"[VOICE SIM] Speaking: {text}")
        return True
    
    def get_status(self):
        return {
            "microphone": False,
            "text_to_speech": False,
            "speech_recognition": False,
            "simulated": True
        }

# Test the class
if __name__ == "__main__":
    print("[VOICE MODULE] Testing voice processor...")
    
    # Try real processor first
    vcp = VoiceCommandProcessor()
    status = vcp.get_status()
    print(f"[VOICE STATUS] {status}")
    
    # Only test listening if microphone is available
    if status["microphone"]:
        print("[VOICE] Ready. Say 'test omega' to check microphone.")
        result = vcp.listen_command(timeout=3)  # Shorter timeout for test
        print(f"[VOICE] Result: {result}")
    else:
        print("[VOICE] Microphone not available - using simulated input")
        sim = SimulatedVoiceProcessor()
        result = sim.listen_command()
        print(f"[VOICE SIM] Result: {result}")
    
    # Test speaking
    if status["text_to_speech"]:
        vcp.speak("Voice module activated. Project Omega is ready.")
    else:
        print("[VOICE] TTS not available - text output only")
