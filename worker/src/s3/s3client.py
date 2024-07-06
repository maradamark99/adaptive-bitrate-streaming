import subprocess
from abc import ABC, abstractmethod
from .s3config import MinioConfig


class S3CmdClientWrapper(ABC):

    @abstractmethod
    def _get_cmd(self, bucket: str, obj: str):
        pass

    def piping_upload(self, bucket: str, obj: str, proc):
        with subprocess.Popen(proc, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
            subprocess.run(self._get_cmd(bucket, obj), stdin=p.stdout)


class MinioCmdClientWrapper(S3CmdClientWrapper):

    def __init__(self, config: MinioConfig):
        self.config = config

    def _get_cmd(self, bucket: str, obj: str):
        return ["mc", "pipe", f"{self.config.load_alias()}/{bucket}/{obj}"]