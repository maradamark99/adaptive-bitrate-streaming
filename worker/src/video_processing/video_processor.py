from abc import ABC, abstractmethod
from typing import Dict
from util import VideoLocation
from video_processing.options import TranscodingOptions, VideoSegmentingOptions
from video_processing.video_metadata import Resolution


class VideoProcessor(ABC):

    @abstractmethod
    def process(self,
                vid_loc: VideoLocation,
                resolutions: list[Resolution],
                transcoding_options: TranscodingOptions,
                segmenting_options: VideoSegmentingOptions
                ) -> Dict[Resolution, list[str]]:
        pass
