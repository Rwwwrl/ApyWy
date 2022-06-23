import abc
from typing import List

from . import repositories
from .. import static_funcs
from ..domain import entities


class BaseInitializer:

    repository: repositories.BaseRepository

    _has_been_initialized: bool = False

    @classmethod
    def _add_to_storage(cls, entities: List) -> None:
        '''перенос проинициализованных объектов в self.storage'''
        cls.repository.add(entities=entities)

    @classmethod
    @abc.abstractmethod
    def get_entities(cls) -> List:
        '''инициализация объектов'''
        raise NotImplementedError

    @classmethod
    def ready(cls) -> None:
        '''инициализация объектов и перенос их в storage'''
        if not cls._has_been_initialized:
            entities = cls.get_entities()
            cls._add_to_storage(entities=entities)
            cls._has_been_initialized = True


class UrlsInitializer(BaseInitializer):
    '''
    Класс, в котором происходит инициализация
    '''
    repository = repositories.UrlsRepository    # type: ignore

    @classmethod
    def get_entities(cls) -> List:
        return static_funcs.get_all_urlpatterns()


class ViewsInitializer(BaseInitializer):
    '''
    Класс, в котором происходит инициализация вьюшек
    '''
    repository = repositories.ViewsRepository    # type: ignore

    @classmethod
    def get_entities(cls) -> List:
        # для полученя вьюшек, нужно сначала получить все юрлы
        UrlsInitializer.ready()
        urls = UrlsInitializer.repository.all()    # type: ignore
        return static_funcs.get_all_view_classes(urlpatterns=urls)


class NamespacesInitializer(BaseInitializer):
    '''
    Класс, в котором происходит инициализация и хранение всех NameSpace
    '''
    repository = repositories.NamespacesRepository    # type: ignore

    @classmethod
    def get_entities(cls) -> List:
        ViewsInitializer.ready()
        namespaces = list(entities.NameSpace._instances.values())
        return namespaces
