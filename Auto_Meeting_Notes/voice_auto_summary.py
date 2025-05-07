import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import openai

# === CONFIGURATION ===
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
OUTPUT_DIR = os.path.expanduser("~/Documents/MeetingNotes")
client = openai.OpenAI(api_key="")  # Replace with your actual API key

class VoiceFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".m4a"):
            return
        
        filename = os.path.basename(event.src_path)
        print(f"📥 Detected new file: {filename}")
        
        full_path = os.path.join(DOWNLOAD_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        transcript_path = os.path.join(OUTPUT_DIR, base_name + ".txt")
        summary_path = os.path.join(OUTPUT_DIR, base_name + "_bulletpoints.txt")

        # === STEP 1: Transcribe with Whisper ===
        print("🎙️ Transcribing with Whisper...")
        subprocess.run([
            "whisper",
            full_path,
            "--language", "Turkish",
            "--output_format", "txt",
            "--output_dir", OUTPUT_DIR
        ])
        print(f"📝 Transcription saved to: {transcript_path}")

        # === STEP 2: Read the transcript ===
        try:
            with open(transcript_path, "r") as f:
                transcript = f.read()
        except FileNotFoundError:
            print("❌ Transcription file not found.")
            return

        # === STEP 3: Send to ChatGPT ===
        print("💬 Sending to ChatGPT...")
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Here is a meeting transcript:\n\n{transcript}\n\nGive the bullet points of the meeting."}
                ]
            )
            summary = response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error from OpenAI: {e}")
            return

        # === STEP 4: Save the summary ===
        with open(summary_path, "w") as f:
            f.write(summary)
        print(f"✅ Summary saved to: {summary_path}")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    event_handler = VoiceFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOAD_DIR, recursive=False)
    observer.start()
    print("👂 Listening for new voice files in Downloads...")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()