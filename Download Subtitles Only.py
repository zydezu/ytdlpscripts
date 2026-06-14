from shared import prompt_link, run_ytdlp, start_downloading

link = prompt_link("video")
start_downloading()
run_ytdlp("--skip-download", link, "--restrict-filenames --write-sub")
