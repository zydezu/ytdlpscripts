from shared import prompt_link, start_downloading, run_ytdlp

link = prompt_link("video")
start_downloading()
run_ytdlp("--skip-download", link, "--restrict-filenames --write-sub")
