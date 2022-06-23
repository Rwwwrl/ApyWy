from typing import List


class BaseRepository:
    '''
    класс, в котором происходит храние проинициализированных объектов по атрибуту attr_name.
    '''
    attr_name: str = ''

    @classmethod
    def add(cls, entities: List) -> None:
        '''добавить *entities в хранение по атрибуту attr_name'''
        storage: list = getattr(cls, cls.attr_name, [])
        if storage:
            storage.extend(entities)
        else:
            setattr(cls, cls.attr_name, list(entities))

    @classmethod
    def all(cls) -> List:
        return getattr(cls, cls.attr_name, [])


class UrlsRepository(BaseRepository):

    attr_name: str = 'urls'


class ViewsRepository(BaseRepository):

    attr_name: str = 'views'


class NamespacesRepository(BaseRepository):

    attr_name: str = 'namespaces'
