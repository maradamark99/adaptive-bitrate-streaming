import subprocess
import ffmpeg
import os
from typing import Dict
from multiprocessing import Pool
from .ffmpeg_video_saving_strategy import FFMpegVideoSavingStrategy
from util import VideoLocation, get_ffmpeg_video_codec_name
from video_processing.video_metadata import Resolution
from video_processing.options import TranscodingOptions, VideoSegmentingOptions
from video_processing.video_processor import VideoProcessor


class FFMpegWrapper(VideoProcessor):

    def __init__(self, video_saving_strategy: FFMpegVideoSavingStrategy = None):
        self.video_saving_strategy = video_saving_strategy

    def transcode(self,
                  to_transcode: str,
                  options: TranscodingOptions):
        if self.video_saving_strategy is None:
            raise AttributeError("Video saving strategy not specified") 
        with Pool() as pool:
            pool.starmap(self._do_transcode, [(res, to_transcode, options, self.video_saving_strategy) for res in options.resolutions])
    
    def _do_transcode(self,
                      resolution: Resolution,
                      to_transcode: str,
                      options: TranscodingOptions,
                      video_saving_strategy: FFMpegVideoSavingStrategy):
        stream = ffmpeg.input(to_transcode).filter("scale", resolution)
        video_saving_strategy.save(to_transcode, stream, options)

    def process(
            self,
            vid_loc: VideoLocation,
            resolutions: list[Resolution], 
            transcoding_options: TranscodingOptions, 
            segmenting_options: VideoSegmentingOptions, 
        ) -> Dict[Resolution, list[str]]:

            save_path = vid_loc.out_video_path_prefix
            os.makedirs(save_path, exist_ok=True)

            result = dict()
            for res in resolutions:
                result[res] = []

            with Pool() as pool:
                pool.starmap(self._do_process, [(vid_loc, res, transcoding_options, segmenting_options) for res in resolutions])
            
            files = os.listdir(save_path)
            for f in files:
                for res in resolutions:
                    if str(res) in f:
                        result.get(res).append(f)

            return result


    def _do_process(self, 
                    vid_loc: VideoLocation,
                    resolution: Resolution, 
                    transcoding_options: TranscodingOptions, 
                    segmenting_options: VideoSegmentingOptions
                ):
        
        bitrate = transcoding_options.bitrates_in_kb_per_sec[resolution]
        codec = get_ffmpeg_video_codec_name(transcoding_options.codec)
        
        output_name = f"{vid_loc.out_video_path_prefix}/{vid_loc.video_name}_{resolution}_%03d.{transcoding_options.output_format}"
        cmd = [
            "ffmpeg",
            "-i", vid_loc.in_video_path,
            "-c:a", "aac",
            "-b:a", "128k",
            "-ac", "1", "-ar", "44100",
            "-c:v", codec,
            "-pix_fmt", "yuv420p",
            "-crf", "21",
            "-map", "0",
            "-s", str(resolution),
            "-maxrate", f"{bitrate}k",
            "-bufsize", f"{bitrate * 2}k",
            "-segment_time", str(segmenting_options.segment_length),
            "-reset_timestamps", "1",
            "-sc_threshold", "0",
            "-force_key_frames", "expr:gte(t,n_forced*1)",
            "-f", "segment",
            output_name
        ]
        subprocess.run(cmd)
