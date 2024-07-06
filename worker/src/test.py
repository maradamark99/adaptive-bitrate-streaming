from minio import Minio
from ffmpegwrapper.ffmpegwrapper import FFMpegWrapper
from ffmpegwrapper.ffprobewrapper import FFProbeWrapper
from s3.s3config import MinioConfig
from streaming_protocol.hls import Hls
from video_processing.video_metadata import Resolution
from worker import WorkResult, Worker


def upload_files(files: list[WorkResult], s3client: Minio):
    for file in files:
        s3client.fput_object("stream", file.video_name, file.video_path )


config = MinioConfig.from_env()
s3client = Minio(config.endpoint, config.access_key, config.secret_key, secure=False)
ffprobe = FFProbeWrapper()
ffmpeg = FFMpegWrapper()
hls = Hls(ffprobe)
worker = Worker(hls, ffprobe, ffmpeg)

files = worker.work(
    "http://localhost:9000/test/test.mp4",
    [Resolution(320,240), Resolution(640,480), Resolution(1280,720)]
)

upload_files(files, s3client)

