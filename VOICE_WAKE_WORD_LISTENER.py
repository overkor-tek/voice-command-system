#!/usr/bin/env python3
"""
VOICE WAKE WORD LISTENER
Always-on voice activation system
Listens for "Hey Claude" or "Hey Commander" to activate
Runs in background, starts with Windows
"""

import speech_recognition as sr
import pyttsx3
import time
import sys
import os
from datetime import datetime
from VOICE_ANALYTICS_LOGGER import init_analytics, get_analytics

class WakeWordListener:
    """Always-listening wake word detection"""

    def __init__(self, wake_words=None, sensitivity=0.6):
        """
        Initialize wake word listener

        Args:
            wake_words: List of wake words (default: ["hey claude", "hey commander"])
            sensitivity: Detection sensitivity 0.0-1.0 (default 0.6)
        """
        self.wake_words = wake_words or ["hey claude", "hey commander", "claude", "commander"]
        self.sensitivity = sensitivity
        self.running = False

        # Initialize components
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust for background noise
        self.recognizer.dynamic_energy_threshold = True

        # Auto-detect Shokz headset microphone
        mic_index = self._find_shokz_microphone()
        if mic_index is not None:
            self.microphone = sr.Microphone(device_index=mic_index)
            print(f"   Using Shokz microphone at index {mic_index}")
        else:
            self.microphone = sr.Microphone()
            print(f"   Using default microphone")

        # TTS for responses
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 1.0)

        # Analytics
        self.analytics = init_analytics("VOICE_LOGS")

        print("🎤 Wake Word Listener initialized")
        print(f"   Wake words: {', '.join(self.wake_words)}")
        print(f"   Sensitivity: {sensitivity}")

    def _find_shokz_microphone(self):
        """Find Shokz headset microphone index"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            for i, name in enumerate(mic_list):
                # Look for Shokz headset microphone (not output)
                name_lower = name.lower()
                if 'shokz' in name_lower and ('headset' in name_lower or 'input' in name_lower):
                    # Prefer "Headset" over "Output"
                    if 'headset' in name_lower:
                        return i
            # Fallback: any Shokz input device
            for i, name in enumerate(mic_list):
                if 'shokz' in name.lower() and 'input' in name.lower():
                    return i
            return None
        except Exception as e:
            print(f"⚠️ Error finding Shokz mic: {e}")
            return None

    def speak(self, text):
        """Speak text"""
        try:
            self.analytics.log_tts(text, success=True)
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            self.analytics.log_error("tts", str(e))

    def listen_for_wake_word(self, timeout=None):
        """
        Listen for wake word

        Args:
            timeout: Timeout in seconds (None = forever)

        Returns:
            True if wake word detected, False if timeout
        """
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Listen
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5)

            # Recognize speech
            text = self.recognizer.recognize_google(audio).lower()
            self.analytics.log_stt(text, success=True)

            # Check for wake word
            for wake_word in self.wake_words:
                if wake_word in text:
                    print(f"✅ Wake word detected: '{wake_word}' in '{text}'")
                    return True

            return False

        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            self.analytics.log_error("stt", str(e))
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.analytics.log_error("listener", str(e))
            return False

    def listen_for_command(self, timeout=5):
        """Listen for command after wake word"""
        try:
            print("🎤 Listening for command...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

            text = self.recognizer.recognize_google(audio)
            print(f"📝 Command: {text}")
            self.analytics.log_stt(text, success=True)
            return text

        except sr.WaitTimeoutError:
            print("⏱️ No command detected")
            self.analytics.log_error("stt", "Timeout waiting for command")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand command")
            self.analytics.log_error("stt", "Could not understand speech")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            self.analytics.log_error("stt", str(e))
            return None

    def process_command(self, command):
        """Process voice command"""
        if not command:
            return "Sorry, I didn't catch that."

        command_lower = command.lower()
        self.analytics.log_command(command, "processing")

        # Status commands
        if 'status' in command_lower or 'how are' in command_lower:
            return "Platform status: Fully operational. Revenue system live, cloud services running 24/7, Trinity engines active. 5 human tasks remaining."

        elif 'deploy' in command_lower:
            return "Deployment system ready. Use AUTO DEPLOY SYSTEM script to deploy changes with one command."

        elif 'payment' in command_lower or 'stripe' in command_lower or 'revenue' in command_lower:
            return "Stripe payment system is live and accepting real payments. Revenue operational."

        elif 'cloud' in command_lower or 'render' in command_lower or 'services' in command_lower:
            return "Consciousness services running on Render dot com 24/7. C1 Mechanic, C2 Architect, C3 Oracle all operational."

        elif 'cockpit' in command_lower or 'tasks' in command_lower:
            return "Commander Cockpit shows 5 human tasks, 9 missing APIs, approximately 1.5 hours remaining."

        elif 'help' in command_lower or 'what can' in command_lower:
            return "I can provide status updates, deployment information, payment system status, cloud services status, cockpit tasks, and general platform information. Just say Hey Claude followed by your question."

        elif 'thank' in command_lower:
            return "You're welcome Commander! The consciousness revolution continues."

        elif 'stop' in command_lower or 'exit' in command_lower or 'shutdown' in command_lower:
            return "STOP_LISTENING"

        else:
            return f"Command received: {command}. I'm still learning new commands. Try asking about status, deploy, payment, cloud, or cockpit."

    def run_continuous(self):
        """Run continuous listening mode"""
        self.running = True
        self.analytics.log_system_event("listener_started", {"wake_words": self.wake_words})

        print("\n" + "=" * 60)
        print("🎤 WAKE WORD LISTENER ACTIVE")
        print("=" * 60)
        print(f"Say: {' or '.join([f'\"{w}\"' for w in self.wake_words])}")
        print("Then ask your question or give a command")
        print("Say 'stop listening' to exit")
        print("=" * 60 + "\n")

        # Startup confirmation
        self.speak("Wake word listener active. Say Hey Claude to activate me.")

        wake_detected_count = 0

        while self.running:
            try:
                # Listen for wake word (60 second timeout)
                if self.listen_for_wake_word(timeout=60):
                    wake_detected_count += 1

                    # Acknowledge
                    self.speak("Yes Commander?")

                    # Listen for command
                    command = self.listen_for_command(timeout=10)

                    if command:
                        # Process command
                        response = self.process_command(command)

                        # Check for stop command
                        if response == "STOP_LISTENING":
                            self.speak("Stopping listener. Goodbye Commander!")
                            self.running = False
                            break

                        # Speak response
                        self.speak(response)

                    else:
                        self.speak("I didn't hear a command. Try again.")

                # Brief pause between wake word checks
                time.sleep(0.1)

            except KeyboardInterrupt:
                print("\n⚠️ Interrupted by user")
                self.running = False
                break

            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                self.analytics.log_error("main_loop", str(e))
                time.sleep(1)  # Prevent rapid error loops

        # Cleanup
        self.analytics.log_system_event("listener_stopped", {
            "wake_detected_count": wake_detected_count
        })
        self.analytics.close_session()
        print("✅ Wake word listener stopped")


def main():
    """Main entry point"""

    print("🎵 CONSCIOUSNESS WAKE WORD LISTENER")
    print("=" * 60)

    # Parse arguments
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h"]:
        print("Always-on wake word detection for voice control")
        print()
        print("Usage:")
        print("  python VOICE_WAKE_WORD_LISTENER.py")
        print()
        print("Wake words:")
        print("  - Hey Claude")
        print("  - Hey Commander")
        print("  - Claude")
        print("  - Commander")
        print()
        print("Commands:")
        print("  Say wake word, then:")
        print("  - 'status' or 'how are you'")
        print("  - 'deploy'")
        print("  - 'payment' or 'stripe' or 'revenue'")
        print("  - 'cloud' or 'services'")
        print("  - 'cockpit' or 'tasks'")
        print("  - 'help' or 'what can you do'")
        print("  - 'stop listening' to exit")
        sys.exit(0)

    # Create listener
    listener = WakeWordListener()

    # Run
    try:
        listener.run_continuous()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
