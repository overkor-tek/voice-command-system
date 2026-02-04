# Voice Command System

**Hands-free AI interaction for desktop -- talk to your consciousness system.**

A modular voice interface that listens for wake words, routes spoken commands to the right AI agent, and speaks responses back. Designed for always-on, hands-free operation with support for desktop microphones, Shokz bone conduction headsets, and Samsung S24 mobile integration.

---

## What It Does

- Listens continuously for configurable wake words ("Hey Claude", "Hey Commander")
- Converts speech to text using Google Speech Recognition
- Routes commands to specialized AI agents based on keyword context
- Speaks responses back using text-to-speech
- Logs every voice interaction with full analytics and session transcripts
- Supports mobile phone voice input via Samsung S24 and ADB

## Features

| Feature | Module | Description |
|---------|--------|-------------|
| Wake Word Detection | `VOICE_WAKE_WORD_LISTENER.py` | Always-on listener with Shokz headset auto-detection |
| Voice Routing | `VOICE_ROUTER_SYSTEM.py` | Routes commands to the right AI agent by keyword matching |
| TTS / STT | `CONSCIOUSNESS_VOICE_MODULE.py` | Text-to-speech and speech-to-text with conversation mode |
| Analytics | `VOICE_ANALYTICS_LOGGER.py` | Session logging, transcripts, and performance reports |
| Mobile Commands | `S24_VOICE_COMMAND_SYSTEM.py` | Samsung S24 voice control via ADB |

## Requirements

- Python 3.8+
- A working microphone (built-in, USB, or Shokz headset)
- Internet connection (for Google Speech Recognition)

### Python Dependencies

```
SpeechRecognition>=3.10.0
pyttsx3>=2.90
PyAudio>=0.2.13
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/overkillkulture/voice-command-system.git
cd voice-command-system
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Platform-Specific Notes for PyAudio

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

## Usage

### Wake Word Listener (Primary Entry Point)

Start the always-on listener. Say "Hey Claude" or "Hey Commander" to activate, then speak your command.

```bash
python VOICE_WAKE_WORD_LISTENER.py
```

Available voice commands after activation:
- **"status"** -- Get system status
- **"deploy"** -- Deployment info
- **"payment" / "stripe"** -- Payment system status
- **"cloud" / "services"** -- Cloud services status
- **"cockpit" / "tasks"** -- View pending tasks
- **"help"** -- List available commands
- **"stop listening"** -- Exit voice mode

### Voice Module (TTS and STT)

Use the core voice module directly for text-to-speech, speech-to-text, or interactive conversation.

```bash
# Speak text aloud
python CONSCIOUSNESS_VOICE_MODULE.py speak "Hello Commander"

# Listen for a single phrase
python CONSCIOUSNESS_VOICE_MODULE.py listen

# Interactive conversation mode
python CONSCIOUSNESS_VOICE_MODULE.py conversation

# List available TTS voices
python CONSCIOUSNESS_VOICE_MODULE.py voices

# Adjust speech rate and volume
python CONSCIOUSNESS_VOICE_MODULE.py --rate 175 --volume 1.0 speak "Hello"
```

### Voice Router (Multi-Agent Routing)

Routes spoken commands to specialized agents based on keyword detection. Multiple agents can respond to a single command.

```bash
python VOICE_ROUTER_SYSTEM.py
```

Keyword routing:
| Keywords | Agent |
|----------|-------|
| security, password, hack | Security Bot |
| build, create, deploy | C1 Mechanic |
| design, architecture, plan | C2 Architect |
| pattern, predict, analyze | C3 Oracle |
| mesh, radio, frequency | Comms Bot |
| help, what, how | General Assistant |

### Samsung S24 Voice Commands

Control the system from your phone via ADB. Supports single-command and continuous-listening modes.

```bash
python S24_VOICE_COMMAND_SYSTEM.py
```

### Analytics Logger

Every voice session is automatically logged. Run standalone to test:

```bash
python VOICE_ANALYTICS_LOGGER.py
```

Session data is saved to the `VOICE_LOGS/` directory:
- `session_<id>.json` -- Full event log
- `transcript_<id>.txt` -- Human-readable transcript
- `report_<id>.txt` -- Session analytics summary

## Configuration

### Custom Wake Words

Edit the wake words in `VOICE_WAKE_WORD_LISTENER.py`:

```python
self.wake_words = ["hey claude", "hey commander", "claude", "commander"]
```

### Shokz Headset Support

The wake word listener automatically detects Shokz bone conduction headsets and selects them as the preferred microphone input. No configuration needed.

### Microphone Sensitivity

Adjust the energy threshold for noisy environments:

```python
self.recognizer.energy_threshold = 4000  # Higher = less sensitive
self.recognizer.dynamic_energy_threshold = True  # Auto-adjust
```

## Project Structure

```
voice-command-system/
  CONSCIOUSNESS_VOICE_MODULE.py   -- Core TTS/STT engine
  VOICE_WAKE_WORD_LISTENER.py     -- Always-on wake word detection
  VOICE_ROUTER_SYSTEM.py          -- Multi-agent command routing
  VOICE_ANALYTICS_LOGGER.py       -- Session logging and analytics
  S24_VOICE_COMMAND_SYSTEM.py     -- Samsung S24 mobile integration
  requirements.txt                -- Python dependencies
  README.md                       -- This file
```

## Links

- **Main Platform:** [https://conciousnessrevolution.io](https://conciousnessrevolution.io)
- **Bug Reports:** [https://conciousnessrevolution.io/bugs.html](https://conciousnessrevolution.io/bugs.html)
- **GitHub:** [https://github.com/overkillkulture](https://github.com/overkillkulture)

## Contributing

Contributions are welcome. Here is how to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b your-feature`
3. Make your changes
4. Submit a pull request back to `main`

For bug reports, open an issue or use the bug report page at [https://conciousnessrevolution.io/bugs.html](https://conciousnessrevolution.io/bugs.html).

## License

MIT License

Copyright (c) 2025 Consciousness Revolution

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
