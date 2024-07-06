import pika
from pika.channel import Channel
from ffmpegwrapper import FFMpegWrapper, S3VideoSavingStrategy
from s3 import MinioCmdClientWrapper, MinioConfig
from streaming_protocol import Hls
from video_processing.video_metadata_extractor import FFProbe
from worker import Worker

metadata_extractor = FFProbe()
config = MinioConfig()
s3client = MinioCmdClientWrapper(config.load_alias())
transcoder = FFMpegWrapper(S3VideoSavingStrategy(s3client))
worker = Worker(metadata_extractor, Hls(transcoder, ...))


def receive(channel: Channel, method, properties, body):
    print(body)


if __name__ == "__main__":
    conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = conn.channel()
    channel.queue_declare(queue='test')
    channel.basic_consume(queue='test', on_message_callback=receive, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
  