from .video_metadata import VideoMetadata
from abc import ABC, abstractmethod


class VideoMetadataExtractor(ABC):

    @abstractmethod
    def extract(self, video: str) -> VideoMetadata | None: 
        pass



