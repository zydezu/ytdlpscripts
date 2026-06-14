from shared import prompt_link, start_downloading, run_ytdlp

link = prompt_link("video")
start_downloading()
quality = '-f "bestvideo[height<=144][vcodec^=avc][ext=mp4][format_note!*=AI-upscaled]+worstaudio/worstvideo+worstaudio" --remux mp4'
run_ytdlp(quality, link, "--restrict-filenames --write-subs --embed-subs")
