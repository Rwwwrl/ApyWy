from typing import List, Optional, Tuple, Union

from django.conf import settings
from django.urls.resolvers import URLPattern, URLResolver

from .entities import NameSpace, View

BUILDIN_NAMESPACES_TO_IGNORE = ('apywy', 'admin')
USER_DECLARED_NAMESPACES_TO_IGNORE: Tuple = getattr(settings, 'NAMESPACES_TO_IGNORE', tuple())


def check_is_namespace_name_in_ignore(namespace_name: str) -> bool:
    '''
    проверяет, находится ли namespace с именем namespace_name в игноре для ApyWy
    '''
    if USER_DECLARED_NAMESPACES_TO_IGNORE == ('*', ):
        return True

    namespaces = BUILDIN_NAMESPACES_TO_IGNORE + USER_DECLARED_NAMESPACES_TO_IGNORE
    return namespace_name in namespaces


def get_all_urlpatterns() -> List[Union[URLPattern, URLResolver]]:
    '''
    получить все urlpatterns в проекте
    '''
    from importlib import import_module
    root_urlconf = import_module(settings.ROOT_URLCONF)
    return root_urlconf.urlpatterns


def get_all_view_classes(urlpatterns: List[Union[URLPattern, URLResolver]]) -> List[View]:
    '''
    Для всех переданных urlpatterns получить их вьюшки. Работает рекурсивно,
    если встретили URLResolver.
    '''
    VIEW_CLASSES = []

    namespace: Optional[NameSpace] = None
    _root: Optional[str] = None

    def inner(urlpatterns: List[Union[URLPattern, URLResolver]]) -> List[View]:
        nonlocal namespace, _root

        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                namespace_name = str(pattern.namespace)
                _root = pattern.pattern._route
                if not check_is_namespace_name_in_ignore(namespace_name=namespace_name):
                    namespace = NameSpace(namespace_name=namespace_name)
                    inner(pattern.url_patterns)
            elif isinstance(pattern, URLPattern):
                view_class = pattern.callback.view_class
                path_to_view = pattern.pattern
                path_to_view._root = _root
                view_class = View(view_class=view_class, url_path=path_to_view)
                namespace.append(view_class)    # type: ignore
                VIEW_CLASSES.append(view_class)
        return VIEW_CLASSES

    return inner(urlpatterns)
