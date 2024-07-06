from typing import Dict
from util import VideoLocation
from streaming_protocol.streaming_protocol import StreamingProtocol
from video_processing.options import TranscodingOptions, VideoSegmentingOptions
from video_processing.video_metadata import Resolution, VideoCodec, VideoMetadata
from video_processing.video_metadata_extractor import VideoMetadataExtractor


class Hls(StreamingProtocol):

    def __init__(self, metadata_extractor: VideoMetadataExtractor):
        self.extractor = metadata_extractor        
    
    def create_transcoding_options(self) -> TranscodingOptions:

        bitrates = dict()
        bitrates[Resolution(320,240)] = 400
        bitrates[Resolution(640,480)] = 1000
        bitrates[Resolution(1280,720)] = 2500
        bitrates[Resolution(1920,1080)] = 7000

        return TranscodingOptions(
            output_format="ts", 
            codec=VideoCodec.H264,
            bitrates_in_kb_per_sec= bitrates,
            two_pass=False 
        )

    def create_segmenting_options(self) -> VideoSegmentingOptions:
        return VideoSegmentingOptions(segment_length=4)

    def create_playlist(self, vid_loc: VideoLocation, segments: Dict[Resolution, list[str]]) -> list[str]:
    
        master_playlist = f"{vid_loc.video_name}_master.m3u8"

        playlist = [master_playlist]
        with open(f"{vid_loc.out_video_path_prefix}/{master_playlist}", mode='w+') as f:
            f.write("#EXTM3U\n")
            keys = segments.keys()
            for i, res in enumerate(keys):
                curr = segments.get(res)[0]
                curr_metadata = self.extractor.extract(f"{vid_loc.out_video_path_prefix}/{curr}")
                f.write(f"#EXT-X-STREAM-INF:BANDWIDTH={curr_metadata.bitrate_in_kb_per_sec * 1024},RESOLUTION={curr_metadata.resolution}\n")
                
                res_segments = segments.get(res)
                res_playlist_name = f"{vid_loc.video_name}_{i}.m3u8"

                playlist.append(res_playlist_name)
                self._create_playlist_for_resolution(f"{vid_loc.out_video_path_prefix}/{res_playlist_name}", vid_loc.out_video_path_prefix, res_segments)
                f.write(res_playlist_name + "\n")

        return playlist

    def _create_playlist_for_resolution(self, playlist_name: str, segment_prefix: str, segments: list[str]):
        sorted_segments = sorted(segments)
        metadatas = self._extract_metadata_from_segments(segment_prefix, sorted_segments)
        with open(playlist_name, mode='w+') as f:
            f.write("#EXTM3U\n")
            f.write("#EXT-X-PLAYLIST-TYPE:VOD\n")
            f.write(f"#EXT-X-TARGETDURATION:{self._get_max_segment_length(metadatas) + 1}\n")
            f.write("#EXT-X-VERSION:4\n")
            f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
            for i, segment in enumerate(sorted_segments):
                f.write(f"#EXTINF:{metadatas[i].length_in_secs},\n")
                f.write(f"{segment}\n")
                
    def _extract_metadata_from_segments(self, segment_prefix: str, segments: list[str]) -> list[VideoMetadata]:
        res_seg_metadata = []
        for j in segments:
            metadata = self.extractor.extract(f"{segment_prefix}/{j}")
            res_seg_metadata.append(metadata)
        return res_seg_metadata

    def _get_max_segment_length(self, metadatas: list[VideoMetadata]) -> float:
        return max(metadatas, key=lambda x: x.length_in_secs).length_in_secs