from dataclasses import dataclass
from enum import Enum


class VideoCodec(Enum):
  AV1 = 1,
  H263 = 2,
  H264 = 3,
  H265 = 4,
  MP4VES = 5,
  MPEG1 = 6,
  MPEG2 = 7

  @staticmethod
  def from_str(value: str):
    value = value.lower()
    if value == 'av1':
      return VideoCodec.AV1
    if value in ('h263', 'h-263'):
      return VideoCodec.H263
    if value in ('avc', 'h264', 'h-264'):
      return VideoCodec.H264
    if value in ('hevc', 'h265', 'h-265'):
      return VideoCodec.H265
    if value in ('mp4ves', 'mp4v-es'):
      return VideoCodec.MP4VES
    if value in ('mpeg1', 'mpeg-1'):
      return VideoCodec.MPEG1
    if value in ('mpeg2', 'mpeg-2'):
      return VideoCodec.MPEG2
    raise ValueError('codec does not exist') 
    

@dataclass
class Resolution:
  width: int
  height: int

  def __str__(self):
    return f"{self.width}x{self.height}"


@dataclass
class VideoMetadata:
  codec: VideoCodec
  resolution: Resolution
  bitrate_in_kb_per_sec: int
  framerate: float
#  length_in_secs: float


