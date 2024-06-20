import subprocess
from video_meta_data_extractor import FFProbe

ext = FFProbe()
metadata = ext.extract("http://localhost:9000/test/test.mp4")
print(metadata)


# # Define resolutions
# resolutions = [
#     {"name": "240p", "scale": "320x240"},
#     {"name": "480p", "scale": "640x480"},
#     {"name": "720p", "scale": "1280x720"},
# ]

# for resolution in resolutions:
#   # Build ffmpeg command with scaling filter
#   ffmpeg_cmd = [
#       "ffmpeg", "-i", "http://localhost:9000/test/test.mp4", 
#       "-vf", f"scale={resolution['scale']}",
#       "-c:v", "libx264", "-crf", "23",  # Adjust CRF for quality (lower is better)
#       "-f", "mp4", "-movflags", "frag_keyframe+empty_moov", "pipe:"
#   ]

#   # Build mc command with output filename
#   mc_cmd = ["mc", "pipe", f"mine/test/{resolution['name']}_output.mp4"]

#   with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE) as ffmpeg_process:
#     subprocess.run(mc_cmd, stdin=ffmpeg_process.stdout)

#   print(f"Finished converting to {resolution['name']}")