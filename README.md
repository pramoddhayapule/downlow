# downlow
A Dieter Rams-inspired media extraction tool and converter powered by yt-dlp, FFmpeg, and Streamlit.
# T-41 // Media Fetch

A minimalist web interface for media extraction and audio conversion powered by `Streamlit`, `yt-dlp`, and `FFmpeg`.

Designed following Dieter Rams' core principle: *"Less, but better"* (*Weniger, aber besser*).

---

## Features

- **Adaptive Resolution Discovery:** Automatically inspects and lists only the resolutions natively available for the provided URL.
- **Audio Extraction:** High-bitrate MP3 extraction with embedded stream merging via FFmpeg.
- **Live Stream Telemetry:** Real-time progress bar, transfer speeds, downloaded size, and remaining time (ETA).
- **Zero Distraction UI:** Minimalist typography and a distraction-free layout.

---

## System Requirements

Before running locally or deploying, ensure the following tools are installed:

1. **Python 3.10+**
2. **FFmpeg** (required for multiplexing audio and video streams)
3. **Node.js** or **Deno** (required by `yt-dlp` for modern stream signature extraction)

---

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
   cd <YOUR_REPO_NAME>
