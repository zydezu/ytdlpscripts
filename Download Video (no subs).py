from shared import prompt_link, run_ytdlp, start_downloading

link = prompt_link("video")
start_downloading()
quality = '-f "bestvideo[format_note!*=AI-upscaled]+bestaudio/bestvideo+bestaudio/best" --remux mp4'
run_ytdlp(quality, link, "--restrict-filenames")
