#!/usr/bin/env python3
"""
VOICE ANALYTICS LOGGER
Tracks all voice interactions, transcriptions, and system events
Creates detailed logs for debugging and analytics
"""

import json
import os
from datetime import datetime
from pathlib import Path

class VoiceAnalytics:
    """Log and analyze all voice interactions"""

    def __init__(self, log_dir="VOICE_LOGS"):
        """Initialize analytics logger"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Session info
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.log_dir / f"session_{self.session_id}.json"
        self.transcript_file = self.log_dir / f"transcript_{self.session_id}.txt"

        # Session data
        self.session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "events": [],
            "statistics": {
                "tts_events": 0,
                "stt_events": 0,
                "commands_processed": 0,
                "errors": 0,
                "total_chars_spoken": 0,
                "total_chars_heard": 0,
                "avg_response_time": 0
            }
        }

        print(f"📊 Voice Analytics initialized")
        print(f"   Session ID: {self.session_id}")
        print(f"   Log file: {self.session_file}")
        print(f"   Transcript: {self.transcript_file}")

    def log_event(self, event_type, data):
        """Log a voice event"""
        timestamp = datetime.now().isoformat()

        event = {
            "timestamp": timestamp,
            "type": event_type,
            "data": data
        }

        self.session_data["events"].append(event)

        # Update statistics
        if event_type == "tts":
            self.session_data["statistics"]["tts_events"] += 1
            self.session_data["statistics"]["total_chars_spoken"] += len(data.get("text", ""))
        elif event_type == "stt":
            self.session_data["statistics"]["stt_events"] += 1
            self.session_data["statistics"]["total_chars_heard"] += len(data.get("text", ""))
        elif event_type == "command":
            self.session_data["statistics"]["commands_processed"] += 1
        elif event_type == "error":
            self.session_data["statistics"]["errors"] += 1

        # Save immediately (for crash recovery)
        self._save()

        # Print to console
        self._print_event(event_type, data)

    def log_tts(self, text, duration=None, success=True):
        """Log text-to-speech event"""
        self.log_event("tts", {
            "text": text,
            "chars": len(text),
            "duration": duration,
            "success": success
        })

        # Add to transcript
        self._append_transcript(f"[CLAUDE] {text}\n\n")

    def log_stt(self, text, confidence=None, duration=None, success=True):
        """Log speech-to-text event"""
        self.log_event("stt", {
            "text": text,
            "chars": len(text) if text else 0,
            "confidence": confidence,
            "duration": duration,
            "success": success
        })

        # Add to transcript
        if text:
            self._append_transcript(f"[COMMANDER] {text}\n\n")

    def log_command(self, command, response, processing_time=None):
        """Log command processing"""
        self.log_event("command", {
            "command": command,
            "response": response,
            "processing_time": processing_time
        })

    def log_error(self, error_type, message, details=None):
        """Log error"""
        self.log_event("error", {
            "error_type": error_type,
            "message": message,
            "details": details
        })

    def log_system_event(self, event_name, details=None):
        """Log system event (startup, shutdown, etc.)"""
        self.log_event("system", {
            "event": event_name,
            "details": details
        })

    def _print_event(self, event_type, data):
        """Print event to console"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        if event_type == "tts":
            text = data.get("text", "")[:50] + "..." if len(data.get("text", "")) > 50 else data.get("text", "")
            print(f"[{timestamp}] 🔊 TTS: {text} ({data.get('chars')} chars)")

        elif event_type == "stt":
            text = data.get("text", "(no text)")
            print(f"[{timestamp}] 🎤 STT: {text} ({data.get('chars')} chars)")

        elif event_type == "command":
            print(f"[{timestamp}] ⚡ CMD: {data.get('command')}")

        elif event_type == "error":
            print(f"[{timestamp}] ❌ ERR: {data.get('error_type')} - {data.get('message')}")

        elif event_type == "system":
            print(f"[{timestamp}] 🔧 SYS: {data.get('event')}")

    def _append_transcript(self, text):
        """Append to transcript file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.transcript_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {text}")

    def _save(self):
        """Save session data to file"""
        self.session_data["last_updated"] = datetime.now().isoformat()

        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2)

    def get_statistics(self):
        """Get session statistics"""
        return self.session_data["statistics"]

    def generate_report(self):
        """Generate session report"""
        stats = self.session_data["statistics"]
        duration = (datetime.now() - datetime.fromisoformat(self.session_data["start_time"])).total_seconds()

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           VOICE SESSION ANALYTICS REPORT                     ║
╚══════════════════════════════════════════════════════════════╝

Session ID: {self.session_id}
Duration: {duration:.1f} seconds

📊 EVENT STATISTICS:
  • TTS Events: {stats['tts_events']}
  • STT Events: {stats['stt_events']}
  • Commands: {stats['commands_processed']}
  • Errors: {stats['errors']}

💬 TEXT STATISTICS:
  • Characters Spoken (Claude): {stats['total_chars_spoken']:,}
  • Characters Heard (Commander): {stats['total_chars_heard']:,}
  • Total Characters: {stats['total_chars_spoken'] + stats['total_chars_heard']:,}

📈 PERFORMANCE:
  • Events per minute: {(len(self.session_data['events']) / (duration / 60)):.1f}
  • Success rate: {((stats['tts_events'] + stats['stt_events'] - stats['errors']) / max(stats['tts_events'] + stats['stt_events'], 1) * 100):.1f}%

📁 FILES:
  • Session log: {self.session_file}
  • Transcript: {self.transcript_file}

╚══════════════════════════════════════════════════════════════╝
"""
        return report

    def close_session(self):
        """Close session and save final data"""
        self.session_data["end_time"] = datetime.now().isoformat()
        self._save()

        # Generate final report
        report = self.generate_report()
        print(report)

        # Save report to file
        report_file = self.log_dir / f"report_{self.session_id}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        return report


# Global analytics instance
_analytics = None

def get_analytics():
    """Get or create global analytics instance"""
    global _analytics
    if _analytics is None:
        _analytics = VoiceAnalytics()
    return _analytics

def init_analytics(log_dir="VOICE_LOGS"):
    """Initialize analytics"""
    global _analytics
    _analytics = VoiceAnalytics(log_dir)
    return _analytics

def close_analytics():
    """Close analytics session"""
    global _analytics
    if _analytics:
        _analytics.close_session()
        _analytics = None


if __name__ == "__main__":
    # Test analytics
    print("🧪 Testing Voice Analytics...")

    analytics = VoiceAnalytics()

    # Simulate some events
    analytics.log_system_event("test_start", {"mode": "testing"})
    analytics.log_tts("Hello Commander! This is a test message.", duration=2.5, success=True)
    analytics.log_stt("What is the platform status?", confidence=0.95, duration=1.2, success=True)
    analytics.log_command("status", "Platform operational", processing_time=0.1)
    analytics.log_tts("Platform status: Fully operational. All systems running.", duration=3.0, success=True)
    analytics.log_error("connection", "Network timeout", {"retry": True})
    analytics.log_system_event("test_end", {"status": "success"})

    # Generate report
    print("\n" + analytics.generate_report())

    # Close session
    analytics.close_session()
