#!/usr/bin/env python3
"""
CONSCIOUSNESS VOICE MODULE
Complete voice integration for Consciousness Revolution platform
Includes TTS (Claude speaks), STT (Commander speaks), and voice commands
"""

import pyttsx3
import speech_recognition as sr
import sys
import os
import re
import time
from pathlib import Path

class ConsciousnessVoice:
    """Voice interface for consciousness revolution"""

    def __init__(self, rate=175, volume=1.0, voice_index=0, enable_analytics=True):
        """Initialize voice system"""
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index
        self.tts_engine = None
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.analytics = None

        # Initialize analytics
        if enable_analytics:
            try:
                from VOICE_ANALYTICS_LOGGER import init_analytics
                self.analytics = init_analytics()
            except Exception as e:
                print(f"⚠️ Analytics disabled: {e}")

        # Initialize TTS
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if voice_index < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_index].id)
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            print("✅ TTS initialized")
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")

        # Initialize microphone
        try:
            self.microphone = sr.Microphone()
            print("✅ Microphone initialized")
        except Exception as e:
            print(f"⚠️ Microphone initialization failed: {e}")

    def clean_text_for_speech(self, text):
        """Remove markdown and special characters for better speech"""
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', ' code block ', text)

        # Remove inline code
        text = re.sub(r'`[^`]+`', ' code ', text)

        # Remove markdown headers
        text = re.sub(r'#{1,6}\s+', '', text)

        # Remove markdown bold/italic
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)

        # Remove bullets and numbers
        text = re.sub(r'^\s*[-*•]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

        # Remove URLs
        text = re.sub(r'https?://[^\s]+', ' link ', text)

        # Remove emojis (basic)
        text = re.sub(r'[🔥💰✅❌⚡🌟🚀🎯📊⏳🟡🟢🔴👽🌌💡🎉🤖🔊📢💬🎵🎶]', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def speak(self, text, interrupt=False):
        """
        Speak text using TTS

        Args:
            text: Text to speak
            interrupt: Stop current speech and start new
        """
        if not self.tts_engine:
            print("❌ TTS not available")
            if self.analytics:
                self.analytics.log_error("tts", "TTS engine not initialized")
            return False

        try:
            if interrupt:
                self.tts_engine.stop()

            clean = self.clean_text_for_speech(text)
            print(f"🔊 Claude speaking: {len(clean)} chars...")

            import time
            start_time = time.time()
            self.tts_engine.say(clean)
            self.tts_engine.runAndWait()
            duration = time.time() - start_time

            print("✅ Done speaking")

            if self.analytics:
                self.analytics.log_tts(clean, duration=duration, success=True)

            return True

        except Exception as e:
            print(f"❌ TTS Error: {e}")
            if self.analytics:
                self.analytics.log_error("tts", str(e))
            return False

    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for voice input

        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Max seconds for phrase

        Returns:
            Recognized text or None
        """
        if not self.microphone:
            print("❌ Microphone not available")
            if self.analytics:
                self.analytics.log_error("stt", "Microphone not initialized")
            return None

        try:
            import time
            start_time = time.time()

            with self.microphone as source:
                print("🎤 Listening... (speak now)")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            print("🧠 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            duration = time.time() - start_time

            print(f"✅ You said: {text}")

            if self.analytics:
                self.analytics.log_stt(text, duration=duration, success=True)

            return text

        except sr.WaitTimeoutError:
            print("⏱️ No speech detected")
            if self.analytics:
                self.analytics.log_error("stt", "Timeout - no speech detected")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            if self.analytics:
                self.analytics.log_error("stt", "Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            if self.analytics:
                self.analytics.log_error("stt", f"Recognition API error: {e}")
            return None
        except Exception as e:
            print(f"❌ Listen error: {e}")
            if self.analytics:
                self.analytics.log_error("stt", str(e))
            return None

    def conversation_mode(self, max_exchanges=10):
        """
        Interactive conversation mode

        Args:
            max_exchanges: Max number of back-and-forth exchanges
        """
        self.speak("Hello Commander! Voice mode activated. Say 'exit' to quit.")

        exchanges = 0
        while exchanges < max_exchanges:
            # Listen for command
            command = self.listen()

            if command is None:
                continue

            # Check for exit
            if 'exit' in command.lower() or 'quit' in command.lower():
                self.speak("Voice mode deactivated. Goodbye Commander!")
                break

            # Process command (placeholder - integrate with consciousness system)
            response = self.process_command(command)
            self.speak(response)

            exchanges += 1

        if exchanges >= max_exchanges:
            self.speak(f"Max exchanges reached. Voice mode deactivating.")

    def process_command(self, command):
        """
        Process voice command (integrate with consciousness system)

        Args:
            command: Recognized text

        Returns:
            Response text
        """
        command_lower = command.lower()

        # Status commands
        if 'status' in command_lower:
            return "Platform status: Fully operational. 5 human tasks remaining, revenue system live."

        elif 'deploy' in command_lower:
            return "Deployment system ready. Use AUTO DEPLOY SYSTEM script."

        elif 'payment' in command_lower or 'stripe' in command_lower:
            return "Stripe payment system is live and accepting real payments."

        elif 'cloud' in command_lower or 'render' in command_lower:
            return "Consciousness services running on Render dot com 24/7."

        elif 'help' in command_lower:
            return "Available commands: status, deploy, payment, cloud, cockpit, services."

        elif 'cockpit' in command_lower:
            return "Commander Cockpit shows 5 human tasks, 9 missing APIs, 1.5 hours remaining."

        elif 'services' in command_lower or 'trinity' in command_lower:
            return "Trinity engines operational. C1 Mechanic, C2 Architect, C3 Oracle running."

        else:
            return f"Command received: {command}. Processing capability coming soon."

    def read_file(self, file_path):
        """Read a file and speak it"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            self.speak(text)
        except FileNotFoundError:
            self.speak(f"File not found: {file_path}")
        except Exception as e:
            self.speak(f"Error reading file: {str(e)}")

    def list_voices(self):
        """List available TTS voices"""
        if not self.tts_engine:
            print("❌ TTS not available")
            return

        try:
            voices = self.tts_engine.getProperty('voices')
            print(f"📢 Available Voices ({len(voices)}):")
            for i, voice in enumerate(voices):
                print(f"  [{i}] {voice.name}")
                print(f"      ID: {voice.id}")
                print(f"      Languages: {voice.languages}")
                print()
        except Exception as e:
            print(f"❌ Error listing voices: {e}")


def main():
    """Main function with command line interface"""

    print("🎵 CONSCIOUSNESS VOICE MODULE")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python CONSCIOUSNESS_VOICE_MODULE.py speak \"Text\"")
        print("  python CONSCIOUSNESS_VOICE_MODULE.py listen")
        print("  python CONSCIOUSNESS_VOICE_MODULE.py conversation")
        print("  python CONSCIOUSNESS_VOICE_MODULE.py read file.txt")
        print("  python CONSCIOUSNESS_VOICE_MODULE.py voices")
        print()
        print("Options:")
        print("  --rate 175      Speech rate (default 175)")
        print("  --volume 1.0    Volume 0.0-1.0 (default 1.0)")
        print("  --voice 0       Voice index (default 0)")
        sys.exit(1)

    # Parse options
    kwargs = {}
    i = 1
    while i < len(sys.argv) and sys.argv[i].startswith('--'):
        if sys.argv[i] == '--rate' and i + 1 < len(sys.argv):
            kwargs['rate'] = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--volume' and i + 1 < len(sys.argv):
            kwargs['volume'] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--voice' and i + 1 < len(sys.argv):
            kwargs['voice_index'] = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Initialize voice
    voice = ConsciousnessVoice(**kwargs)

    # Get command
    if i >= len(sys.argv):
        print("❌ No command specified")
        sys.exit(1)

    command = sys.argv[i]

    # Execute command
    if command == "speak" and i + 1 < len(sys.argv):
        text = sys.argv[i + 1]
        voice.speak(text)

    elif command == "listen":
        result = voice.listen()
        if result:
            print(f"📝 Recognized: {result}")

    elif command == "conversation":
        voice.conversation_mode()

    elif command == "read" and i + 1 < len(sys.argv):
        file_path = sys.argv[i + 1]
        voice.read_file(file_path)

    elif command == "voices":
        voice.list_voices()

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
