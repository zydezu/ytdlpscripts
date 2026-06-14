import subprocess

from shared import prompt_link, start_downloading

link = prompt_link("image")
start_downloading()
subprocess.run(
    [
        "gallery-dl",
        "-d",
        "downloads (images)",
        "--cookies",
        "cookies.txt",
        "--ugoira",
        "mp4",
        link,
    ]
)
