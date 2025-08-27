from src.database.crud.base import CRUDBaseTasks
from src.database.models.models import Category

class CRUDCategory(CRUDBaseTasks[Category]):
    pass

category_crud = CRUDCategory(Category) # объект класса Category для работы с категориями