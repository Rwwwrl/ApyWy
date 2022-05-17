from typing import List, Optional, Union

from django.urls.resolvers import URLPattern, URLResolver

from .entities import NameSpace, View

BUILDIN_APPS_TO_IGNORE = ('admin', )


def get_all_urlpatterns() -> List[Union[URLPattern, URLResolver]]:
    '''
    получить все urlpatterns в проекте
    '''
    from django.conf import settings
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

    def inner(urlpatterns: List[Union[URLPattern, URLResolver]]) -> List[View]:
        nonlocal namespace

        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                if pattern.app_name not in BUILDIN_APPS_TO_IGNORE:
                    namespace = NameSpace(namespace_name=str(pattern.namespace))
                    inner(pattern.url_patterns)
            elif isinstance(pattern, URLPattern):
                view_class = pattern.callback.view_class
                url_path_to_view = str(pattern.pattern)
                view_class = View(view_class=view_class, url_path=url_path_to_view)
                namespace.append(view_class)    # type: ignore
                VIEW_CLASSES.append(view_class)
        return VIEW_CLASSES

    return inner(urlpatterns)
