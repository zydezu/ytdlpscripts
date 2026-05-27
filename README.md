# ytdlp Downloader Scripts

A collection of convenience wrapper scripts around [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [gallery-dl](https://github.com/mikf/gallery-dl), along with other utilities for downloading videos, audio, subtitles, comments, and images from online platforms.

## Features

- **Video downloading** — best quality, worst quality, or pick your resolution; with or without subtitles
- **Audio extraction** — best quality or MP3-converted, with thumbnail embedding
- **Subtitle & comment downloading** — standalone scripts for subtitles (including SRV3) and comments
- **Image downloading** — download from Pixiv, Twitter, Instagram, Reddit, etc. via `gallery-dl`
- **Auto-detect mode** — smart routing: yt-dlp for video links, gallery-dl for image links
- **File upload** — upload to a personal server with MOV→MP4 remux, auto-thumbnail with watermark, Discord embed HTML generation, and clipboard copy
- **Archive update** — batch re-download metadata/comments for previously archived videos
- **AutoHotkey integration** — `Ctrl+Alt+U` for auto-download, `Ctrl+Alt+T` for file upload

## Requirements

- **Python >= 3.14**
- **FFmpeg** (required for format conversion, thumbnail generation)
- **libsvtav1** (optional, for AVIF conversion)
- **AutoHotkey v2** (optional, for hotkey automation on Windows)

## Installation

```bash
git clone https://github.com/zydezu/ytdlpscripts
cd ytdlp
pip install -r requirements.txt
# or, if using uv:
uv sync
```

Keep yt-dlp itself up to date:

```bash
pip install -U --pre "yt-dlp[default]"
```

or with your package manager.

Place a `cookies.txt` file (Netscape format) in the project root for authenticated access.

## Usage

All scripts are interactive — run them and paste a URL when prompted.

| Command | Description |
|---|---|
| `python "Download Video.py"` | Best quality video with subtitles & metadata |
| `python "Download Video (no subs).py"` | Best quality video, no subtitles |
| `python "Download Video (pick resolution).py"` | Video with a user-chosen max resolution |
| `python "Download Video (avif).py"` | Download + convert to AVIF |
| `python "Download Video (gif).py"` | Download + convert to GIF |
| `python "Download Worst Video.py"` | Lowest quality (≤144p, AVC) |
| `python "Download Audio (Best).py"` | Best audio quality with thumbnail |
| `python "Download Audio (mp3).py"` | Audio converted to MP3 |
| `python "Download Subtitles Only.py"` | Download subtitles only |
| `python "Download srv3 Subtitles Only.py"` | Download SRV3 subtitles only |
| `python "Download Comments.py"` | Download video comments |
| `python "Download Image.py"` | Download images via gallery-dl |
| `python "Auto Determine.py"` | Auto-detect video/image and download |
| `python "Upload File.py"` | Upload a file to your personal server |
| `python "Update Archive.py"` | Re-download metadata for archived videos |

## Dependencies

- `yt-dlp` — core video/audio download engine
- `gallery-dl` — image gallery download engine
- `mutagen` — audio metadata embedding
- `Pillow` — image processing (thumbnails, watermarks)
- `pyperclip` / `pywin32` — clipboard access
- `requests` — HTTP for uploads
- `click` — CLI utilities
- `bs4` — HTML parsing (khinsider)
- `ttconv` — TTML→SRT conversion
- `certifi`, `urllib3`, `idna`, `charset-normalizer`, etc.

## Configuration

- **yt-dlp.conf** — global yt-dlp options (e.g., remote EJS components)
- **uploadurl.txt** — upload server URL (gitignored)
- **uploadlogin.txt** — upload credentials (gitignored)
- **cookies.txt** — Netscape-format cookies for authenticated sessions

## Credits

The `khinsider/` subdirectory is a fork of [@obskyr](https://github.com/obskyr/khinsider).
