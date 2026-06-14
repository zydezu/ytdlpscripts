from shared import (
    bcolors,
    convert_to_avif,
    get_latest_mp4,
    prompt_link,
    run_ytdlp,
    start_downloading,
)

link = prompt_link("video")
start_downloading()
quality = '-f "bestvideo[format_note!*=AI-upscaled]+bestaudio/bestvideo+bestaudio/best" --remux mp4'
run_ytdlp(quality, link, "--add-metadata --write-subs --embed-subs --embed-thumbnail")

mp4 = get_latest_mp4()
if mp4:
    convert_to_avif(mp4)
else:
    print(f"{bcolors.WARNING}No MP4 file found to convert.{bcolors.ENDC}")
