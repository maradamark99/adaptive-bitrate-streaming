from typing import Dict
from dataclasses import dataclass
from .video_metadata import Resolution, VideoCodec


@dataclass
class VideoSegmentingOptions:
	segment_length: int


@dataclass
class TranscodingOptions:

    bitrates_in_kb_per_sec: Dict[Resolution, int]
    codec: VideoCodec
    output_format: str
    two_pass: bool = False # this might be ffmpeg specific 

    # TODO: add validation
    # TODO: add hw accel