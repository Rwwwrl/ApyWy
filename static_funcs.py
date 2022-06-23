from typing import Dict, List, Optional, Tuple, Union

from django.conf import settings
from django.urls.resolvers import URLPattern, URLResolver

from .domain.entities import NameSpace, View

BUILDIN_NAMESPACES_TO_IGNORE = ('apywy', 'admin')
USER_DECLARED_NAMESPACES_TO_IGNORE: Tuple = getattr(settings, 'NAMESPACES_TO_IGNORE', tuple())


def check_is_namespace_name_in_ignore(namespace_name: str) -> bool:
    '''
    проверяет, находится ли namespace с именем namespace_name в игноре для apywy
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

    # при двух разных юрлах на одну вьюшку, схема будет дублироваться. Это мы избегаем
    already_added_django_views = set()

    namespace: Optional[NameSpace] = None
    _root: Optional[str] = None

    def inner(urlpatterns: List[Union[URLPattern, URLResolver]]) -> List[View]:
        nonlocal namespace, _root

        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                namespace_name = str(pattern.namespace)

                try:
                    _root = pattern.pattern._route
                except AttributeError:
                    _root = None

                if not check_is_namespace_name_in_ignore(namespace_name=namespace_name):
                    namespace = NameSpace(namespace_name=namespace_name)
                    inner(pattern.url_patterns)
            elif isinstance(pattern, URLPattern):
                try:
                    # мы не умеем работать с func-based views, поэтому просто их скипаем
                    django_view_class = pattern.callback.view_class
                except AttributeError:
                    continue

                path_to_view = pattern.pattern
                path_to_view._root = _root
                view_class = View(django_view_class=django_view_class, url_path=path_to_view)

                if django_view_class in already_added_django_views:
                    view_class.append_url_path(url_path=path_to_view)
                    continue
                already_added_django_views.add(django_view_class)

                namespace.append(view_class)    # type: ignore
                VIEW_CLASSES.append(view_class)
        return VIEW_CLASSES

    return inner(urlpatterns)


def get_paths_data_of_view(view: View) -> List[Dict]:
    '''
    получить список полных путей и их наименовай до всех юрлов у вьюшки
    '''
    result = []
    for url_path in view.url_paths:
        url_path_data = {}
        url_path_data['url_name'] = url_path.name
        url_path_data['url_full_path'] = url_path._root + str(url_path)
        result.append(url_path_data)
    return result
