import os
import tempfile
import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="T-41 // Media Fetch",
    page_icon="⚪",
    layout="centered"
)

# Dieter Rams / Braun-inspired minimalist styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F4F4F2;
        color: #1A1A1A;
    }
    
    h1 {
        font-weight: 500 !important;
        letter-spacing: -0.04em !important;
        font-size: 1.8rem !important;
        color: #1A1A1A !important;
        margin-bottom: 0.2rem !important;
    }
    .caption {
        font-size: 0.8rem;
        color: #7A7A78;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    .metric-row {
        font-family: 'Space Grotesk', monospace;
        font-size: 0.85rem;
        color: #555555;
        margin-top: 0.4rem;
        letter-spacing: 0.02em;
    }

    /* Minimal Input Fields */
    .stTextInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D1CD !important;
        border-radius: 2px !important;
        color: #111111 !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #EA580C !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 2px !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.2rem !important;
    }
    .stButton>button:hover {
        background-color: #EA580C !important;
    }
    .stDownloadButton>button {
        background-color: #EA580C !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 2px !important;
        font-weight: 500 !important;
        width: 100%;
    }

    /* Minimal orange progress bar accent */
    .stProgress > div > div > div > div {
        background-color: #EA580C !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("T-41 // Transceiver")
st.markdown('<div class="caption">Audio-Visual Extraction Tool — Rams Form 02</div>', unsafe_allow_html=True)

url = st.text_input("Source URL", placeholder="Paste YouTube link here...")

# Base extractor options that circumvent 403 Forbidden on cloud IPs
BASE_YTDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'http_chunk_size': 10485760,  # 10MB chunks prevent stream timeout
    'extractor_args': {
        'youtube': {
            'player_client': ['ios', 'android', 'mweb']
        }
    }
}

def get_video_formats(video_url):
    with yt_dlp.YoutubeDL(BASE_YTDL_OPTS) as ydl:
        info = ydl.extract_info(video_url, download=False)
        formats = info.get('formats', [])
        resolutions = set()
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('height'):
                resolutions.add(f.get('height'))
        sorted_res = sorted(list(resolutions), reverse=True)
        return info.get('title'), sorted_res

if url:
    try:
        with st.spinner("Inspecting media formats..."):
            title, resolutions = get_video_formats(url)

        st.text(f"Media: {title}")

        if resolutions:
            options = [f"{res}p" for res in resolutions]
            options.append("Audio Only (MP3)")

            selected_option = st.selectbox("Resolution Target", options)

            if st.button("Process Media"):
                progress_bar = st.progress(0.0)
                status_text = st.empty()

                def progress_hook(d):
                    if d['status'] == 'downloading':
                        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                        downloaded = d.get('downloaded_bytes', 0)
                        
                        fraction = downloaded / total if total > 0 else 0.0
                        progress_bar.progress(min(max(fraction, 0.0), 1.0))

                        speed_mb = (d.get('speed') or 0) / (1024 * 1024)
                        eta_sec = d.get('eta', 0)
                        
                        eta_str = f"{int(eta_sec)}s" if eta_sec is not None else "--"
                        downloaded_mb = downloaded / (1024 * 1024)
                        total_mb = total / (1024 * 1024)

                        status_text.markdown(
                            f'<div class="metric-row">'
                            f'Progress: {fraction * 100:.1f}% &nbsp;|&nbsp; '
                            f'Downloaded: {downloaded_mb:.1f}/{total_mb:.1f} MB &nbsp;|&nbsp; '
                            f'Speed: {speed_mb:.2f} MB/s &nbsp;|&nbsp; '
                            f'ETA: {eta_str}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                    elif d['status'] == 'finished':
                        progress_bar.progress(1.0)
                        status_text.markdown(
                            '<div class="metric-row">Download complete. Merging streams via FFmpeg...</div>',
                            unsafe_allow_html=True
                        )

                temp_dir = tempfile.mkdtemp()
                
                # Combine base cloud-bypass options with task-specific settings
                ydl_opts = {**BASE_YTDL_OPTS, 'progress_hooks': [progress_hook]}

                if selected_option == "Audio Only (MP3)":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(temp_dir, "%(title)s.%(ext)s"),
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    target_h = selected_option.replace("p", "")
                    ydl_opts.update({
                        'format': f"bestvideo[height<={target_h}]+bestaudio/best[height<={target_h}]/best",
                        'outtmpl': os.path.join(temp_dir, "%(title)s.%(ext)s"),
                        'merge_output_format': 'mp4',
                    })

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    filepath = ydl.prepare_filename(info_dict)
                    
                    if selected_option == "Audio Only (MP3)":
                        filepath = os.path.splitext(filepath)[0] + ".mp3"
                    elif not filepath.endswith(".mp4"):
                        filepath = os.path.splitext(filepath)[0] + ".mp4"

                status_text.markdown('<div class="metric-row" style="color: #EA580C;">✓ Processing complete. Ready for download.</div>', unsafe_allow_html=True)
                
                st.session_state['file_ready'] = filepath
                st.session_state['file_name'] = os.path.basename(filepath)

            if 'file_ready' in st.session_state and os.path.exists(st.session_state['file_ready']):
                with open(st.session_state['file_ready'], "rb") as file:
                    st.download_button(
                        label="Save File to Storage",
                        data=file,
                        file_name=st.session_state['file_name'],
                        mime="audio/mp3" if selected_option == "Audio Only (MP3)" else "video/mp4"
                    )
        else:
            st.warning("No compatible streams found.")

    except Exception as err:
        st.error(f"Execution Error: {err}")