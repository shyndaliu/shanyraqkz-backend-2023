from app.config import database

from .adapters.jwt_service import JwtService
from .adapters.s3_service import S3Service
from .repository.repository import ShanyraksRepository

from ..auth.service import config


class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
        jwt_svc: JwtService,
        s3_service: S3Service,
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = S3Service()


def get_service():
    repository = ShanyraksRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    s3_service = S3Service

    svc = Service(repository, jwt_svc, s3_service)
    return svc
