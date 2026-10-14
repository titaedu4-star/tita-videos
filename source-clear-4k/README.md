# Render the clear 4K video

Requires Python 3.10+, FFmpeg (with libx264), Liberation Sans fonts, and the Cairo system library.

Install Python dependencies: `python -m pip install pillow cairosvg`.

Run `python render.py` from this folder. It generates `timetable-clear-4k.mp4`, an SVG source composition, and timing metadata.

The complete scene is vector art; the timetable entries are illustrative. Resolution: 3840×2160, 10 fps, 3.5 seconds, 20 Mbps H.264 target bitrate, 2.5-second final hold.
