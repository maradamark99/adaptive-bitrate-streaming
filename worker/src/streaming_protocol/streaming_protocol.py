from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict
from util import VideoLocation
from video_processing.options import TranscodingOptions, VideoSegmentingOptions
from video_processing.video_metadata import Resolution


class StreamingProtocolType(Enum):
    HLS = 1
    DASH = 2


class StreamingProtocol(ABC):

    @abstractmethod
    def create_transcoding_options(self) -> TranscodingOptions:
        pass

    @abstractmethod
    def create_segmenting_options(self) -> VideoSegmentingOptions:
        pass

    @abstractmethod
    def create_playlist(self, vid_loc: VideoLocation, segments: Dict[Resolution, list[str]]) -> list[str]:
        pass

