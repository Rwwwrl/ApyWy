from typing import Any, Dict, List

from django.urls.resolvers import URLPattern

from ..utilities.custom_typing import DjangoView


class Singletone:

    _instances: Dict[str, Any] = {}

    def __new__(cls, key: str, *args: Any, **kwargs: Any) -> Any:
        '''
        @param key: str - значение, которое однозначно идентифицирует экземпляр класса,
        нужно для выборки инстанса синглтона.
        '''

        if key in cls._instances:
            return cls._instances[key]
        instance = super().__new__(cls)
        cls._instances[key] = instance
        return instance


class NameSpace(Singletone):
    '''
    класс, который связыват namespace и его views, синглтон
    '''

    _instances: Dict[str, 'NameSpace'] = {}

    def __new__(cls, namespace_name: str, *args: Any, **kwargs: Any) -> "NameSpace":
        return super().__new__(cls, key=namespace_name)

    def __init__(self, namespace_name: str):
        '''
        @param namespace_name: str - имя джанговского namespace
        '''
        self.namespace_name = namespace_name
        self.views: List['View'] = []

    def append(self, view: 'View') -> None:
        self.views.append(view)

    def __repr__(self) -> str:
        return f'<NameSpace: {[str(i) for i in self.views]}>'


class View(Singletone):
    '''
    класс, который связыват класс DjangoView и его url путь, синглтон
    '''

    _instances: Dict[str, 'View'] = {}

    def __new__(cls, view_class: DjangoView, *args: Any, **kwargs: Any) -> 'View':
        view_class_name = view_class.__name__
        return super().__new__(cls, key=view_class_name)

    def __init__(self, view_class: DjangoView, url_path: URLPattern) -> None:
        self.view_class = view_class
        self.url_path = url_path

    def __repr__(self) -> str:
        return f'<View: {self.view_class.__name__}>'
