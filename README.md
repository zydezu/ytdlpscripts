# ytdlp Downloader Scripts

A collection of convenience wrapper scripts around [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [gallery-dl](https://github.com/mikf/gallery-dl), along with other utilities for downloading videos, audio, subtitles, comments, and images from online platforms.

## Features

- **Video downloading** - best quality, worst quality, or pick your resolution; with or without subtitles
- **Audio extraction** - best quality or MP3-converted, with thumbnail embedding
- **Subtitle & comment downloading** - standalone scripts for subtitles (including SRV3) and comments
- **Image downloading** - download from Pixiv, Twitter, Instagram, Reddit, etc. via `gallery-dl`
- **Auto-detect mode** - smart downloading: yt-dlp for video links, gallery-dl for image links
- **Archive update** - batch re-download metadata/comments for previously archived videos

## Requirements

- **Python >= 3.14**
- **FFmpeg** (required for format conversion, thumbnail generation)
- **libsvtav1** (optional, for AVIF conversion)

> [!IMPORTANT]
> On Linux distributions, you may need to install additional dependencies such as `tk` or `python3-tk` for the scripts to work.

## Installation

```bash
git clone <repo-url>
cd ytdlp
pip install -r requirements.txt
# or, if using uv:
uv sync
```

Keep yt-dlp itself up to date (Windows):

```bash
pip install -U --pre "yt-dlp[default]"
```

or update with your package manager.

Place a `cookies.txt` file (Netscape format) in the project root for authenticated access, you can obtain these with an extension like [Get-cookies.txt-LOCALLY](https://github.com/kairi003/Get-cookies.txt-LOCALLY).

## Usage

Below is a list of scripts and what they do. Run them and enter the URL when prompted.

| File | Description |
|---|---|
| `Auto Determine.py` | Auto-detect video/image and download (yt-dlp/gallery-dl) |
| `Download Video.py` | Download the best quality video with subtitles & metadata |
| `Download Video (no subs).py` | Download the best quality video, no subtitles |
| `Download Video (pick resolution).py` | Download the video with a user-chosen max resolution |
| `Download Video (avif).py` | Download and convert to AVIF |
| `Download Video (gif).py` | Download and convert to GIF |
| `Download Worst Video.py` | Download the lowest quality video |
| `Download Audio (Best).py` | Download the best quality audio (usually opus) |
| `Download Audio (mp3).py` | Download audio and convert it to MP3 |
| `Download Subtitles Only.py` | Download subtitles only |
| `Download srv3 Subtitles Only.py` | Download SRV3 (YouTube's custom format) subtitles only |
| `Download Comments.py` | Download the comments from a video |
| `Download Image.py` | Download images via gallery-dl |
| `Update Archive.py` | Re-download metadata for archived videos |

## Dependencies

- `yt-dlp` - core video/audio download engine
- `gallery-dl` - image gallery download engine
- `mutagen` - audio metadata embedding
- `Pillow` - image processing (thumbnails, watermarks)
- `pyperclip` / `pywin32` - clipboard access
- `requests` - HTTP for uploads
- `click` - CLI utilities
- `tk` - GUI utilities
- `bs4` - HTML parsing (khinsider)
- `ttconv` - TTML→SRT conversion
- `certifi`, `urllib3`, `idna`, `charset-normalizer`, etc.

## Configuration

- **yt-dlp.conf** - global yt-dlp options (e.g., remote EJS components)
- **cookies.txt** - Netscape-format cookies for authenticated sessions (required for some sites like Pixiv)

## Credits

The `khinsider/` subdirectory is a fork of [@obskyr](https://github.com/obskyr/khinsider).
