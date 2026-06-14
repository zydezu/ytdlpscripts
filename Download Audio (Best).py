from shared import prompt_link, start_downloading, run_ytdlp

link = prompt_link("audio (can be a video link)")
start_downloading()
run_ytdlp("-x", link, "--embed-thumbnail")
