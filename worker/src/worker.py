from dataclasses import dataclass
from util import VideoLocation, extract_filename_from_path
from video_processing.video_metadata import Resolution
from video_processing.video_metadata_extractor import VideoMetadataExtractor
from streaming_protocol.streaming_protocol import StreamingProtocol
from video_processing.video_processor import VideoProcessor
from itertools import chain

@dataclass
class WorkResult:
    file_path: str
    file_name: str

class Worker:

    def __init__(self, protocol: StreamingProtocol, extractor: VideoMetadataExtractor, vid_processor: VideoProcessor):
        self.extractor = extractor
        self.protocol = protocol
        self.vid_processor = vid_processor

    def work(self, in_video_path: str, resolutions: list[Resolution]) -> list[WorkResult]:
        video_name = extract_filename_from_path(in_video_path)
        vid_loc = VideoLocation(in_video_path=in_video_path, video_name=video_name)
        transcoding_options = self.protocol.create_transcoding_options()
        segmenting_options = self.protocol.create_segmenting_options()
        segments = self.vid_processor.process(vid_loc, resolutions, transcoding_options, segmenting_options)
        playlist = self.protocol.create_playlist(vid_loc, segments)
        segments_list = list(chain.from_iterable([*segments.values()]))
        result = list(map(lambda x: WorkResult(f"{vid_loc.out_video_path_prefix}/{x}", x), segments_list + playlist))
        return result