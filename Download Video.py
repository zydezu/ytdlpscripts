from shared import prompt_link, start_downloading, run_ytdlp

link = prompt_link("video")
start_downloading()
quality = '-f "bestvideo[format_note!*=AI-upscaled]+bestaudio/bestvideo+bestaudio/best" --remux mp4'
run_ytdlp(quality, link, "--add-metadata --write-subs --embed-subs --embed-thumbnail")
