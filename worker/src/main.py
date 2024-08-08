from minio import Minio
import pika
from pika.channel import Channel
from ffmpegwrapper.ffmpegwrapper import FFMpegWrapper
from s3.s3config import MinioConfig
from streaming_protocol.hls import Hls
from ffmpegwrapper.ffprobewrapper import FFProbeWrapper
from video_processing.video_metadata import Resolution
from worker import Worker, WorkResult

metadata_extractor = FFProbeWrapper()
config = MinioConfig.from_env()
s3client = Minio(
    endpoint=config.endpoint,
    access_key=config.access_key,
    secret_key=config.secret_key,
    secure=False
)
video_processor = FFMpegWrapper()
worker = Worker(Hls(metadata_extractor), metadata_extractor, video_processor)

def upload(files: list[WorkResult]):
    for file in files:
        s3client.fput_object("stream", file.file_name, file.file_path)

def receive(channel: Channel, method, properties, body):
    # TODO: get resolutions from the message
    resolutions = [Resolution(320, 240), Resolution(640, 480), Resolution(1280, 720)]
    files = worker.work(str(body, encoding='utf-8'), resolutions)
    upload(files)


if __name__ == "__main__":
    # TODO: get host and queue from environment
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = conn.channel()
    channel.queue_declare(queue='process', durable=True)
    channel.basic_consume(queue='process', on_message_callback=receive, auto_ack=True)
    channel.basic_qos(prefetch_count=1)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    conn.close()