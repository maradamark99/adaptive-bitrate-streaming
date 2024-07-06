from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class MinioConfig:
    endpoint: str
    access_key: str
    secret_key: str

    @staticmethod
    def from_env():
        load_dotenv()
        return MinioConfig(
            endpoint=os.environ["MINIO_ENDPOINT"],
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"]
        )

    @staticmethod
    def load_alias():
        load_dotenv()
        mc_alias = os.getenv("MC_ALIAS")
        if mc_alias is None:
            raise EnvironmentError("No Minio alias found")
        return mc_alias
        
