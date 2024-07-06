import json
import subprocess
from util import get_ffmpeg_video_codec_name
from video_processing.video_metadata import Resolution, VideoMetadata
from video_processing.video_metadata_extractor import VideoMetadataExtractor


class FFProbeWrapper(VideoMetadataExtractor):

    def extract(self, video: str) -> VideoMetadata | None:
        cmd = [
            "ffprobe",
            "-v", 
            "quiet", 
            "-print_format", 
            "json", 
            "-show_format", 
            "-show_streams", 
            video
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)

        return self._parse_probe_result(proc.stdout)

    def _parse_probe_result(self, result: str) -> VideoMetadata | None:
        j = json.loads(result)
        video = j["streams"][0]
        format = j["format"]

        duration = format["duration"]
        bitrate = int(format["bit_rate"]) / 1024
        codec = get_ffmpeg_video_codec_name(video["codec_name"])
        framerate = float(video["avg_frame_rate"].split("/")[0])
        duration = float(format["duration"])

        return VideoMetadata(
            codec=codec,
            resolution=Resolution(int(video["width"]), int(video["height"])),
            bitrate_in_kb_per_sec=bitrate,
            framerate=framerate,
            length_in_secs=duration
        )
    