from app.config import database
from pydantic import BaseSettings

from .adapters.jwt_service import JwtService
from .adapters.s3_service import S3Service
from .repository.repository import ShanyraksRepository

# from .adapters.here_service import HereService

from ..auth.service import config


# lass Config(BaseSettings):
#    HERE_API_KEY: str


# here_api_key = Config()


class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
        jwt_svc: JwtService,
        s3_service: S3Service,
        # here_service: HereService,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = S3Service()
        # self.here_service = HereService


def get_service():
    repository = ShanyraksRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    s3_service = S3Service
    # here_service = HereService(here_api_key.HERE_API_KEY)

    svc = Service(repository, jwt_svc, s3_service)
    return svc
