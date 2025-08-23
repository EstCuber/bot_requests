from src.database.crud.base import CRUDBaseTasks
from src.database.models.models import Service

class CRUDService(CRUDBaseTasks[Service]):
    pass

service_crud = CRUDService(Service)