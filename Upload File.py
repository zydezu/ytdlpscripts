import os, sys, requests, re, subprocess, json, hashlib
import pyperclip
import tkinter as tk
from tkinter import filedialog
import mimetypes
from PIL import Image
os.system("")

TEMPLATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={url}">
    <meta property="og:image" content="{thumbnail_url}">
    <meta property="og:type" content="video.other">
    <meta property="og:video:url" content="{url}">
    <meta property="og:video:width" content="{width}">
    <meta property="og:video:height" content="{height}">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="{url}">{url}</a>...</p>
</body>
</html>
"""

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    LINE = '\033[90m'
    ENDC = '\033[0m'

def get_upload_url(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            url = f.read().strip()
            if url:
                return url

UPLOADURL = get_upload_url("uploadurl.txt")

def copy_url_to_clipboard(url):
    try:
        if sys.platform.startswith("win"):
            pyperclip.copy(url)
        elif sys.platform.startswith("darwin"):
            subprocess.run("pbcopy", text=True, input=url.strip(), check=True)
        else:  # Linux (requires xclip or xsel installed)
            subprocess.run("xclip -selection clipboard", shell=True, text=True, input=url.strip(), check=True)
    except Exception as e:
        print("Failed to copy to clipboard:", e)

def is_video(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith("video")

def create_thumbnail_keyframe(video_path, thumbnail_path, desired_time=2.0):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        capture_output=True, text=True, check=True
    )
    duration = float(result.stdout.strip())

    seek_time = min(1, duration / 2)

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(seek_time),
        "-i", video_path,
        "-vf", r"select=eq(pict_type\,I)",
        "-frames:v", "1",
        thumbnail_path
    ], check=True)

    if not os.path.exists(thumbnail_path) or os.path.getsize(thumbnail_path) == 0:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", video_path,
            "-frames:v", "1",
            thumbnail_path
        ], check=True)

def get_video_dimensions(file_path):
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height",
                "-of", "json",
                file_path
            ],
            capture_output=True,
            text=True,
            check=True
        )
        info = json.loads(result.stdout)
        stream = info['streams'][0]
        width = stream['width']
        height = stream['height']
        return width, height
    except Exception as e:
        print(f"Error getting video dimensions: {e}")
        return None, None

def generate_html_file(url, thumbnail_url, width, height, output_path):
    html_content = TEMPLATE_HTML.format(
        url=url,
        thumbnail_url=thumbnail_url,
        width=width,
        height=height
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML file saved at: {output_path}")

def uniquify_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    hash_suffix = hashlib.md5(filename.encode()).hexdigest()[:5]
    return f"{name}_{hash_suffix}{ext}"

def sanitize_filename(filename: str) -> str:
    filename = filename.replace(" ", "").replace("-", "_")
    filename = re.sub(r"[\[\]{}()<>:\"'`^&*?=+$,;|]", "", filename)
    return filename

def file_exists_on_server(query: str, filename: str) -> bool:
    search_url = f"{UPLOADURL}?simple&q={query}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        files_list = response.text.splitlines()
        return len(files_list) > 0
    except Exception as e:
        print(f"Error checking if file exists: {e}")
        return False

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select the file to upload"
    )
    if not file_path:
        print("No file selected.")
        exit(1)

    print(f"{bcolors.OKBLUE}Uploading...{bcolors.ENDC}")

    filename = sanitize_filename(os.path.basename(file_path))
    if file_exists_on_server(filename, filename):
        filename = uniquify_filename(filename)
    url = f"{UPLOADURL}/uploads/discord/videos/{filename}"

    try:
        subprocess.run(
            ["curl", "--globoff", "-T", file_path, url],
            check=True
        )
        print(f"{bcolors.OKGREEN}Upload complete: {bcolors.WARNING}{url}{bcolors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"Upload failed: {e}")

    if is_video(file_path):
        width, height = get_video_dimensions(file_path)

        thumbnail_filename = filename.rsplit(".", 1)[0] + ".png"  # save as PNG
        thumbnail_url = f"{UPLOADURL}/uploads/discord/thumbnails/{thumbnail_filename}"
        thumbnail_path = os.path.join(os.getcwd(), thumbnail_filename)

        try:
            create_thumbnail_keyframe(file_path, thumbnail_path)
            subprocess.run(["curl", "--globoff", "-T", thumbnail_path, thumbnail_url], check=True)
            print(f"{bcolors.OKGREEN}Thumbnail uploaded: {bcolors.WARNING}{thumbnail_url}{bcolors.ENDC}")
        except subprocess.CalledProcessError as e:
            print(f"Thumbnail upload failed: {e}")

        discord_file_name = filename.rsplit(".", 1)[0] + ".html"

        generate_html_file(url, thumbnail_url, width, height, discord_file_name)

        discord_html_url = f"{UPLOADURL}/uploads/discord/{discord_file_name}"

        try:
            subprocess.run(["curl", "--globoff", "-T", discord_file_name, discord_html_url], check=True)
            print(f"HTML page uploaded: {discord_html_url}")
        except subprocess.CalledProcessError as e:
            print(f"HTML upload failed: {e}")

        try:
            os.remove(discord_file_name)
            print(f"Deleted local HTML file: {discord_file_name}")
            os.remove(thumbnail_filename)
            print(f"Deleted local thumbnail file: {thumbnail_filename}")
        except Exception as e:
            print(f"Error deleting local files: {e}")

        copy_url_to_clipboard(discord_html_url)