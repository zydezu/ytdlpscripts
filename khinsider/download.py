import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from khinsider import (
    NonexistentFormatsError,
    NonexistentSoundtrackError,
    Soundtrack,
    download,
)

BASE_URL = "https://downloads.khinsider.com/"

link = input("Khinsider URL or soundtrack ID: ").strip()

m = re.match(
    r"^https?://"
    + re.escape("downloads.khinsider.com")
    + r"/game-soundtracks/album/(?P<id>[^/]+)/?$",
    link,
    re.IGNORECASE,
)
soundtrack_id = m.group("id") if m else link

fmt = input("Format (e.g. flac, ogg, mp3) [default: flac]: ").strip()
format_order = None
if fmt:
    format_order = [f.strip().lstrip(".").lower() for f in fmt.split(",")]

try:
    success = download(
        soundtrack_id, formatOrder=format_order or ["flac"], verbose=True
    )
    if not success:
        print("\nNot all files could be downloaded.", file=sys.stderr)
        sys.exit(1)
except NonexistentSoundtrackError:
    print(f'Soundtrack "{soundtrack_id}" does not exist.', file=sys.stderr)
    sys.exit(1)
except NonexistentFormatsError as e:
    print(
        f"Format not available. Available: {e.soundtrack.availableFormats}",
        file=sys.stderr,
    )
    sys.exit(1)
except KeyboardInterrupt:
    print("\nStopped.")
    sys.exit(1)
