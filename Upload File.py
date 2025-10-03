import os, sys, requests, re, subprocess, json, uuid
import pyperclip
import tkinter as tk
from tkinter import filedialog
import mimetypes
from PIL import Image, ImageDraw, ImageFont
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADURL = get_upload_url(os.path.join(SCRIPT_DIR, "uploadurl.txt"))

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

def create_thumbnail_keyframe(video_path, thumbnail_path):
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

def get_video_info(file_path):
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            "-show_format",
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
        info = json.loads(result.stdout)

        video_stream = next(
            (s for s in info["streams"] if s["codec_type"] == "video"), None
        )

        if not video_stream:
            raise RuntimeError("No video stream found")

        codec = video_stream.get("codec_name")
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        fps_str = video_stream.get("avg_frame_rate", "0/0")
        fps = eval(fps_str) if fps_str != "0/0" else 0  # safe float fps

        duration = float(info["format"].get("duration", 0))

        return {
            "codec": codec,
            "width": width,
            "height": height,
            "fps": fps,
            "duration": duration,
        }

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffprobe failed: {e.stderr}")

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

def uniquify_filename(filename):
    name, ext = os.path.splitext(filename)
    unique_id = uuid.uuid4().hex[:8]  # first 8 characters of a random UUID
    return f"{name}_{unique_id}{ext}"

def sanitize_filename(filename):
    filename = filename.replace(" ", "").replace("-", "_")
    filename = re.sub(r"[\[\]{}()<>:\"'`^&*?=+$,;|]", "", filename)
    return filename

def file_exists_on_server(query):
    search_url = f"{UPLOADURL}?simple&q={query}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        files_list = response.text.splitlines()
        return len(files_list) > 0
    except Exception as e:
        print(f"Error checking if file exists: {e}")
        return False

def add_text_to_thumbnail(thumbnail_path, text, info):
    if len(text) > 32:
        text = text[:32] + "..."
    text = text
    watermark = f"{info["width"]}x{info["height"]}@{round(info["fps"])}FPS ({info["codec"]}) - files.zydezu.com"

    img = Image.open(thumbnail_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))  # Transparent layer

    draw = ImageDraw.Draw(txt_layer)

    font_size = max(10, int(img.width * 0.03))
    try:
        font = ImageFont.truetype("AOTFShinGoProBold.otf", font_size)  # Adjust size as needed
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 15
    x = img.width - text_width - padding
    y = padding

    outline_width = max(1, font_size // 15)
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            draw.text((x+dx, y+dy), text, font=font, fill=(0,0,0,255))

    draw.text((x, y), text, font=font, fill=(255,255,255,255))

    font_size -= 5
    try:
        font = ImageFont.truetype("AOTFShinGoProMedium.otf", font_size)  # Adjust size as needed
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = img.width - text_width - padding
    y = padding + text_height + 12

    outline_width = max(1, font_size // 15)
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            draw.text((x+dx, y+dy), watermark, font=font, fill=(0,0,0,255))

    draw.text((x, y), watermark, font=font, fill=(255,255,255,255))

    combined = Image.alpha_composite(img, txt_layer)

    try:
        overlay = Image.open("drpeppergirlnobgsz.png").convert("RGBA")
        overlay_width, overlay_height = overlay.size

        # Position bottom-right with padding
        overlay_x = img.width - overlay_width - padding
        overlay_y = img.height - overlay_height + padding

        # Paste overlay with transparency
        combined.paste(overlay, (overlay_x, overlay_y), overlay)
    except Exception as e:
        print(f"Failed to add overlay: {e}")

    combined.convert("RGB").save(thumbnail_path)

if __name__ == "__main__":
    if sys.argv[1:]:
        file_path = sys.argv[1]
    else:
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
    if file_exists_on_server(filename):
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
        info = get_video_info(file_path)

        thumbnail_filename = filename.rsplit(".", 1)[0] + ".png"
        thumbnail_url = f"{UPLOADURL}/uploads/discord/thumbnails/{thumbnail_filename}"
        thumbnail_path = os.path.join(SCRIPT_DIR, thumbnail_filename)

        try:
            create_thumbnail_keyframe(file_path, thumbnail_path)
            add_text_to_thumbnail(thumbnail_path, f"{filename}", info)
            subprocess.run(["curl", "--globoff", "-T", thumbnail_path, thumbnail_url], check=True)
            print(f"{bcolors.OKGREEN}Thumbnail uploaded: {bcolors.WARNING}{thumbnail_url}{bcolors.ENDC}")
        except subprocess.CalledProcessError as e:
            print(f"Thumbnail upload failed: {e}")

        discord_file_name = filename.rsplit(".", 1)[0] + ".html"
        discord_file_path = os.path.join(SCRIPT_DIR, discord_file_name)

        generate_html_file(url, thumbnail_url, info["width"], info["height"], discord_file_path)

        discord_html_url = f"{UPLOADURL}/uploads/discord/{discord_file_name}"

        try:
            subprocess.run(["curl", "--globoff", "-T", discord_file_path, discord_html_url], check=True)
            print(f"HTML page uploaded: {discord_html_url}")
        except subprocess.CalledProcessError as e:
            print(f"HTML upload failed: {e}")

        try:
            os.remove(discord_file_path)
            print(f"Deleted local HTML file: {discord_file_path}")
            os.remove(os.path.join(SCRIPT_DIR, thumbnail_filename))
            print(f"Deleted local thumbnail file: {thumbnail_filename}")
        except Exception as e:
            print(f"Error deleting local files: {e}")

        copy_url_to_clipboard(discord_html_url)