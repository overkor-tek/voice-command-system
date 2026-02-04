#!/usr/bin/env python3
"""
INTELLIGENT VOICE ROUTING SYSTEM
Routes voice input to the right AI agent based on context

When you say "security issue" → Security bot responds
When you say "switch computers" → System bot responds
When you say "build something" → C1 Mechanic responds

All bots listen. Right ones respond. Can talk over each other.
"""

import speech_recognition as sr
import threading
import queue
import time
from datetime import datetime

# Voice input queue (all bots listen to this)
voice_queue = queue.Queue()

# Agent definitions with their keywords
AGENTS = {
    'Security Bot': {
        'keywords': ['security', 'password', 'login', 'auth', 'hack', 'breach', 'vulnerability'],
        'priority': 10,  # High priority
        'color': '\033[91m'  # Red
    },
    'System Bot': {
        'keywords': ['switch', 'computer', 'reboot', 'restart', 'shutdown', 'system'],
        'priority': 9,
        'color': '\033[94m'  # Blue
    },
    'C1 Mechanic': {
        'keywords': ['build', 'create', 'make', 'deploy', 'install', 'setup'],
        'priority': 8,
        'color': '\033[92m'  # Green
    },
    'C2 Architect': {
        'keywords': ['design', 'architecture', 'plan', 'scale', 'optimize'],
        'priority': 8,
        'color': '\033[93m'  # Yellow
    },
    'C3 Oracle': {
        'keywords': ['pattern', 'predict', 'analyze', 'future', 'vision'],
        'priority': 8,
        'color': '\033[95m'  # Magenta
    },
    'Comms Bot': {
        'keywords': ['mesh', 'radio', 'frequency', 'antenna', 'comms', 'communication'],
        'priority': 7,
        'color': '\033[96m'  # Cyan
    },
    'General Assistant': {
        'keywords': ['help', 'what', 'how', 'why', 'when', 'where'],
        'priority': 1,  # Lowest priority (fallback)
        'color': '\033[97m'  # White
    }
}

class VoiceRouter:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.running = True

        # Adjust for ambient noise
        print("🎙️  Calibrating microphone...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Ready to listen!\n")

    def listen_continuous(self):
        """Continuously listen for voice input"""
        with self.microphone as source:
            while self.running:
                try:
                    print("👂 Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)

                    # Transcribe
                    text = self.recognizer.recognize_google(audio)
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    print(f"\n🎤 [{timestamp}] You said: \"{text}\"\n")

                    # Put in queue for all agents to process
                    voice_queue.put({
                        'text': text,
                        'timestamp': timestamp,
                        'audio': audio
                    })

                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    print("❓ Couldn't understand that")
                except sr.RequestError as e:
                    print(f"❌ Error: {e}")
                except KeyboardInterrupt:
                    self.running = False
                    break

    def route_to_agents(self, message):
        """Determine which agents should respond"""
        text = message['text'].lower()
        responding_agents = []

        # Check each agent's keywords
        for agent_name, config in AGENTS.items():
            for keyword in config['keywords']:
                if keyword in text:
                    responding_agents.append({
                        'name': agent_name,
                        'priority': config['priority'],
                        'color': config['color']
                    })
                    break  # Found a match, don't check other keywords

        # Sort by priority (highest first)
        responding_agents.sort(key=lambda x: x['priority'], reverse=True)

        # If no specific agents matched, use General Assistant
        if not responding_agents:
            responding_agents.append({
                'name': 'General Assistant',
                'priority': 1,
                'color': AGENTS['General Assistant']['color']
            })

        return responding_agents

    def agent_response(self, agent_name, color, message_text):
        """Simulate agent response (replace with actual AI call)"""
        responses = {
            'Security Bot': f"🔒 Security analysis: Checking '{message_text}' for vulnerabilities...",
            'System Bot': f"💻 System command recognized. Processing '{message_text}'...",
            'C1 Mechanic': f"🔧 Build request received. Planning '{message_text}'...",
            'C2 Architect': f"🏗️  Architecture analysis for '{message_text}'...",
            'C3 Oracle': f"🔮 Pattern recognition active. Analyzing '{message_text}'...",
            'Comms Bot': f"📡 Communications request. Processing '{message_text}'...",
            'General Assistant': f"💬 I heard '{message_text}'. How can I help?"
        }

        response = responses.get(agent_name, f"Agent {agent_name} processing...")
        print(f"{color}{response}\033[0m")  # Color + reset

    def process_queue(self):
        """Process messages from the voice queue"""
        while self.running:
            try:
                message = voice_queue.get(timeout=1)

                # Route to appropriate agents
                agents = self.route_to_agents(message)

                print(f"📨 Routing to {len(agents)} agent(s):\n")

                # Multiple agents can respond (talking over each other)
                threads = []
                for agent in agents:
                    thread = threading.Thread(
                        target=self.agent_response,
                        args=(agent['name'], agent['color'], message['text'])
                    )
                    thread.start()
                    threads.append(thread)

                # Wait for all agents to finish
                for thread in threads:
                    thread.join()

                print("\n" + "="*60 + "\n")

            except queue.Empty:
                continue
            except KeyboardInterrupt:
                self.running = False
                break

    def run(self):
        """Start the voice routing system"""
        print("🌐 INTELLIGENT VOICE ROUTING SYSTEM")
        print("="*60)
        print("Say commands and watch agents respond contextually!")
        print("\nExamples:")
        print("  'Check security' → Security Bot responds")
        print("  'Build a mesh network' → C1 Mechanic + Comms Bot respond")
        print("  'Design architecture' → C2 Architect responds")
        print("\nPress Ctrl+C to stop\n")
        print("="*60 + "\n")

        # Start queue processor in background
        processor_thread = threading.Thread(target=self.process_queue, daemon=True)
        processor_thread.start()

        # Start listening (blocks until Ctrl+C)
        try:
            self.listen_continuous()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping voice router...")
            self.running = False

if __name__ == "__main__":
    router = VoiceRouter()
    router.run()
