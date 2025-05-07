# 🔣 Voice to Meeting Summary Automation

This Python script automatically watches your **Downloads** folder for new `.m4a` audio files (like voice memos), transcribes them using **Whisper**, summarizes them into bullet points using **OpenAI GPT-4**, and saves the results to your **Documents/MeetingNotes** folder.

---

## ✨ Features

* Automatically detects new `.m4a` files
* Transcribes audio using OpenAI Whisper
* Summarizes meeting content into bullet points with GPT-4
* Saves both the transcript and summary into `~/Documents/MeetingNotes`

---

## 📁 Folder Structure

```
voice-to-summary/
├── voice_auto_summary.py        # Main script
├── run.sh                       # One-click launcher (optional)
├── requirements.txt             # Dependencies
├── README.md                    # This documentation
```

> **Note:** The script saves files in a folder called `MeetingNotes` inside your **Documents** folder. If this folder does not exist, it will be created automatically. You may rename it, but if you do, remember to update this path in the script:

```python
OUTPUT_DIR = os.path.expanduser("~/Documents/MeetingNotes")
```

---

## 🔧 Requirements

* Python 3.8+
* [Whisper CLI](https://github.com/openai/whisper)
* OpenAI Python SDK (>= 1.0.0)
* [ffmpeg](https://ffmpeg.org/download.html)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/voice-to-summary.git
cd voice-to-summary
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Whisper

```bash
pip install git+https://github.com/openai/whisper.git
```

### 4. Install ffmpeg (if not already installed)

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu:**

```bash
sudo apt install ffmpeg
```

### 5. Add your OpenAI API Key

Edit the script and replace:

```python
client = openai.OpenAI(api_key="YOUR_API_KEY")
```

with your actual [OpenAI API key](https://platform.openai.com/account/api-keys).

---

## 🚀 Running the Script

```bash
python voice_auto_summary.py
```

Once running:

* Drop a `.m4a` file into your `Downloads` folder
* The script will transcribe it and save both the `.txt` and bullet point summary to `~/Documents/MeetingNotes`

---

## 📂 Output Example

After processing `New Recording 1.m4a`, you will get:

* `New Recording 1.txt` — full transcript
* `New Recording 1_bulletpoints.txt` — summarized meeting notes

---

## ✅ Optional: One-Click Launcher or App Integration

### 🔍 Create a One-Click `.sh` Launcher

1. Create a file named `run.sh`:

```bash
nano run.sh
```

2. Paste this into the file:

```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 voice_auto_summary.py
```

3. Save and exit (Ctrl+O, Enter, Ctrl+X).

4. Make it executable:

```bash
chmod +x run.sh
```

5. Now run your automation with:

```bash
./run.sh
```

### 💡 Create a macOS App with Automator

1. Open **Automator** and select **"Application"**.
2. Add a **"Run Shell Script"** block.
3. Paste this:

```bash
cd /full/path/to/your/project
./run.sh
```

4. Save the application (e.g., `VoiceSummary.app`).
5. Double-click to launch or add to **Login Items** in System Settings to auto-run at login.

---

## 🖋️ Customize the Assistant Prompt or Output Style

You can change how ChatGPT responds by modifying this part of the code:

```python
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Here is a meeting transcript:\n\n{transcript}\n\nGive the bullet points of the meeting."}
    ]
)
summary = response.choices[0].message.content
```

* Change the **prompt** to adjust formatting, tone, or language
* Use a different model if needed (e.g., `gpt-3.5-turbo`)

---

## 🌐 Change or Detect Language for Transcription

By default, the script transcribes Turkish audio. You can change or detect language by modifying this line:

```python
"--language", "Turkish",
```

### To change to English:

```python
"--language", "English",
```

### To let Whisper auto-detect the language:

Simply **remove** the language option entirely from the command:

```python
subprocess.run([
    "whisper",
    full_path,
    "--output_format", "txt",
    "--output_dir", OUTPUT_DIR
])
```

Whisper will then try to guess the language based on the audio input.

---

## 🤖 Want to Improve This?

Ideas for enhancements:

* GUI version with file picker
* Export to Markdown or PDF
* Support for multiple languages
* Upload summaries to Notion or Google Drive

---

## 📜 License

MIT License

---

## 👨‍💼 Author

Created by Yusuf Mehmet Colak — contributions welcome!

Feel free to submit pull requests or issues to improve this tool!
