from dataclasses import dataclass
from video_processing.video_metadata import VideoCodec


TEMPORARY_STORAGE_PATH='/tmp'

@dataclass
class VideoLocation:
	in_video_path: str
	video_name: str
	temp_storage_path: str = TEMPORARY_STORAGE_PATH

	@property
	def out_video_path_prefix(self):
		return f"{self.temp_storage_path}/{self.video_name}"





def get_ffmpeg_video_codec_name(codec: VideoCodec) -> str:
	match codec:
		case VideoCodec.H264:
			return "libx264"
		case _:
			return "libx264"

def extract_filename_from_path(s: str):
	arr = s.split("/")
	if len(arr) > 0:
		return arr[-1].split(".")[0]
	return s
