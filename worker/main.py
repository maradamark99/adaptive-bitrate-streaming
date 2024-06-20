import pika
import subprocess
from pika.channel import Channel
from multiprocessing import Pool


resolutions = [
    {"name": "240p", "scale": "320x240"},
    {"name": "480p", "scale": "640x480"},
    {"name": "720p", "scale": "1280x720"},
]

def convert_video(resolution):
  ffmpeg_cmd = [
      "ffmpeg", "-i", "http://localhost:9000/test/test.mp4", 
      "-vf", f"scale={resolution['scale']}",
      "-c:v", "libx264", "-crf", "23",  # Adjust CRF for quality (lower is better)
      "-f", "mp4", "-movflags", "frag_keyframe+empty_moov", "pipe:"
  ] 

  mc_cmd = ["mc", "pipe", f"mine/test/{resolution['name']}_output.mp4"]

  with subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE) as ffmpeg_process:
    subprocess.run(mc_cmd, stdin=ffmpeg_process.stdout)

  print(f"Finished converting to {resolution['name']}")

def receive(channel: Channel, method, properties, body):
  print(body)
  # with Pool() as pool:
  # pool.map(convert_video, resolutions)
  

if __name__ == "__main__":
  conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = conn.channel()
  channel.queue_declare(queue='test')
  channel.basic_consume(queue='test', on_message_callback=receive, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  