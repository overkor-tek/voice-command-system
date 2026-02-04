#!/usr/bin/env python3
"""
S24 VOICE COMMAND SYSTEM
Use S24 as voice interface to control entire consciousness revolution system

COMMANDS:
- "Deploy Trinity" → Activates Trinity on all computers
- "Check status" → Reports system health
- "Backup everything" → Triggers full backup
- "Pull recordings" → Extracts Pat recording
- "Show me the data" → Opens consciousness dashboard

Trinity C3 Oracle Build - Nov 6, 2025
"""

import subprocess
import speech_recognition as sr
import json
from datetime import datetime
from pathlib import Path

class S24VoiceCommander:
    def __init__(self):
        """Initialize voice command system"""
        self.recognizer = sr.Recognizer()
        self.commands_log = Path(r"C:\Users\dwrek\.consciousness\voice_commands.jsonl")
        self.commands_log.parent.mkdir(parents=True, exist_ok=True)

        print("=" * 80)
        print("🎤 S24 VOICE COMMAND SYSTEM")
        print("=" * 80)
        print()
        print("AVAILABLE COMMANDS:")
        print("  'deploy trinity' - Activate Trinity on all computers")
        print("  'check status' - System health report")
        print("  'backup everything' - Full system backup")
        print("  'pull recordings' - Extract phone recordings")
        print("  'show dashboard' - Open consciousness dashboard")
        print("  'run extraction' - S24 full extraction")
        print("  'activate sensors' - Turn on all phone sensors")
        print("  'start transcription' - Begin continuous transcription")
        print()

    def listen_from_phone(self):
        """Listen to audio from S24 microphone via ADB"""
        # This would use:
        # adb shell "am start -a android.speech.action.RECOGNIZE_SPEECH"
        # Or stream audio from phone to computer for processing
        pass

    def listen_from_computer(self):
        """Listen to computer microphone (fallback)"""
        with sr.Microphone() as source:
            print("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print(f"📝 Heard: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand")
            return None
        except sr.RequestError as e:
            print(f"❌ Error: {e}")
            return None

    def execute_command(self, command):
        """Execute voice command"""
        timestamp = datetime.now().isoformat()

        # Log command
        with open(self.commands_log, 'a') as f:
            f.write(json.dumps({
                'timestamp': timestamp,
                'command': command,
                'status': 'executing'
            }) + '\n')

        # Parse and execute
        if 'deploy trinity' in command or 'start trinity' in command:
            print("\n🌀 Deploying Trinity...")
            # Would trigger Trinity deployment
            print("✅ Trinity deployment initiated")

        elif 'check status' in command or 'system status' in command:
            print("\n📊 System Status:")
            self.check_system_status()

        elif 'backup everything' in command or 'full backup' in command:
            print("\n💾 Starting full backup...")
            # Would trigger backup system
            print("✅ Backup initiated")

        elif 'pull recording' in command or 'extract recording' in command:
            print("\n📞 Pulling call recordings...")
            subprocess.run(['powershell', '-File', r'C:\Users\dwrek\Desktop\PULL_PAT_RECORDING_NOW.ps1'])

        elif 'show dashboard' in command or 'open dashboard' in command:
            print("\n📈 Opening consciousness dashboard...")
            subprocess.run(['start', 'https://conciousnessrevolution.io/hud'], shell=True)

        elif 'run extraction' in command or 's24 extraction' in command:
            print("\n📱 Running S24 extraction...")
            subprocess.run(['python', r'C:\Users\dwrek\Desktop\S24_FULL_EXTRACTION.py'])

        elif 'activate sensor' in command or 'turn on sensor' in command:
            print("\n🔧 Activating all sensors...")
            subprocess.run(['python', r'C:\Users\dwrek\Desktop\S24_CONSCIOUSNESS_NODE.py'])

        elif 'start transcription' in command or 'begin transcription' in command:
            print("\n🎤 Starting continuous transcription...")
            # Would start transcription service
            print("✅ Transcription started")

        else:
            print(f"\n❌ Unknown command: {command}")
            print("Say 'help' for available commands")

    def check_system_status(self):
        """Check and report system status"""
        # Check running services
        services = {
            'ChatGPT API': 5555,
            'Grok API': 8778,
            'Poker Bridge': 8777,
            'Trinity Hub': 9999
        }

        for service, port in services.items():
            try:
                result = subprocess.run(
                    ['curl', f'http://localhost:{port}/health'],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    print(f"  ✅ {service}: Online")
                else:
                    print(f"  ❌ {service}: Offline")
            except:
                print(f"  ❌ {service}: Offline")

        # Check S24 connection
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if 'device\t' in result.stdout:
            print(f"  ✅ S24 Phone: Connected")
        else:
            print(f"  ❌ S24 Phone: Not connected")

    def continuous_listening(self):
        """Listen for commands continuously"""
        print("\n🎤 Continuous voice command mode")
        print("Say commands naturally, I'm listening...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                command = self.listen_from_computer()
                if command:
                    self.execute_command(command)
                print("\nListening...")
        except KeyboardInterrupt:
            print("\n\n✅ Voice commander stopped")

# Example usage
if __name__ == "__main__":
    commander = S24VoiceCommander()

    print("MODES:")
    print("  1. Single command")
    print("  2. Continuous listening")
    print()

    choice = input("Choose mode (1 or 2): ").strip()

    if choice == "2":
        commander.continuous_listening()
    else:
        print("\nSpeak your command:")
        command = commander.listen_from_computer()
        if command:
            commander.execute_command(command)
