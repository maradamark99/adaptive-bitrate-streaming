import subprocess
import re
from video_metadata import VideoMetadata, VideoCodec, Resolution
from abc import ABC, abstractmethod


class VideoMetadataExtractor(ABC):

  @abstractmethod
  def extract(self, url: str) -> VideoMetadata | None: 
    pass


class FFProbe(VideoMetadataExtractor):

  def extract(self, url: str) -> VideoMetadata | None:
    cmd = ["ffprobe", url]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in iter(proc.stdout.readline, b''):
      decoded = line.decode('utf-8')[:-1]

      if (metadata := self.parse(decoded)) is not None:
        return metadata

  def parse(self, line) -> VideoMetadata | None:
    video_metadata = None
    right_prefix = "Stream: Video:"
    if line.lstrip().startswith(right_prefix):
      line = line[len(right_prefix):]
      
      pattern = r"(\w+)[\w\s\(\)\/]+, [\w\s\(\)]+, (\d+)x(\d+) [\w\s\[\]:]+, (\d+) kb\/s, (\d+) fps"
      result = re.search(pattern, line).groups()
      
      video_metadata = VideoMetadata(
        codec=VideoCodec.from_str(result[0]),
        resolution=Resolution(result[1], result[2]),
        bitrate_in_kb_per_sec=result[3],
        framerate=result[4]
      )
    return video_metadata

