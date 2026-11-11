# Downlow // T-41 Transceiver

A distraction-free media extraction and conversion tool built with `yt-dlp`, `FFmpeg`, and `Streamlit`.

Designed with restraint, following Dieter Rams' ethos: *"Less, but better"*.

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
   git clone https://github.com/pramoddhayapule/downlow.git
   cd downlow
