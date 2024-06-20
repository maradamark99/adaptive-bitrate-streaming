

class Worker:

  def __init__(self, extractor: VideoMetadataExtractor, transcoder: Transcoder):
    self.extractor = extractor
    self.transcoder = transcoder

  def work(self, url: str): None
  