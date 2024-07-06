from s3.s3client import S3CmdClientWrapper
from video_processing.options import TranscodingOptions
from util import get_ffmpeg_video_codec_name


class FFMpegVideoSavingStrategy:

    def save(self, to_transcode: str, stream, options: TranscodingOptions):
        pass

    def _get_args(self, options: TranscodingOptions) -> dict[str, any]:
        bitrate = options.bitrate_in_kb_per_sec if options.bitrate_in_kb_per_sec > 0 else None
        codec = get_ffmpeg_video_codec_name(options.codec)
        args = {
            "format": options.output_format,
            "vcodec": codec,
            "bitrate": bitrate if bitrate is not None else {},
        }
        return args


class S3VideoSavingStrategy(FFMpegVideoSavingStrategy):

    def __init__(self, client: S3CmdClientWrapper):
        self.client = client

    def save(self, to_save: str, stream, options: TranscodingOptions):
        args = self._get_args(options)
        proc = (
            stream
            .output('pipe:', **args)
            .compile(overwrite_output=True)
        )
        bucket, obj = self._parse_to_save(to_save)
        self.client.piping_upload(bucket, obj, proc)

    def _get_args(self, options: TranscodingOptions) -> dict[str, any]:
        args = super()._get_args(options)
        args["movflags"] = "frag_keyframe+empty_moov"
        return args

    def _parse_to_save(self, to_save: str) -> tuple[str, str]:
        s = to_save.split('/')
        if len(s) < 2:
            raise ValueError("Expected a string separated by /")
        return s[0], s[1]


class DiskVideoSavingStrategy(FFMpegVideoSavingStrategy):
    pass