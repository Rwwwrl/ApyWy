from . import entities, static_funcs


class UrlsInitialier:
    '''
    Класс, в котором происходит инициализация и хранение всех urlpatterns
    '''
    @classmethod
    def _configure_urls(cls) -> None:
        project_url_patterns = static_funcs.get_all_urlpatterns()
        cls.URLS = project_url_patterns    # type: ignore

    @classmethod
    def ready(cls) -> None:
        '''
        метод, отвечающий за иницилазацию получения всех urlpatterns
        '''
        if not hasattr(cls, 'URLS'):
            cls._configure_urls()


class ViewsInitializer:
    '''
    Класс, в котором происходит инициализация и хранение всех View
    '''
    @classmethod
    def _configure_views(cls) -> None:
        UrlsInitialier.ready()
        project_views = static_funcs.get_all_view_classes(urlpatterns=UrlsInitialier.URLS)    # type: ignore
        cls.VIEWS = project_views    # type: ignore

    @classmethod
    def ready(cls) -> None:
        '''
        метод, отвечающий за иницилазацию получения всех View
        '''
        if not hasattr(cls, 'VIEWS'):
            cls._configure_views()


class NameSpacesInitializer:
    '''
    Класс, в котором происходит инициализация и хранение всех NameSpace
    '''
    @classmethod
    def _configure_namespace(cls) -> None:
        ViewsInitializer.ready()
        namespaces = entities.NameSpace._instances.values()
        cls.NAMESPACES = namespaces    # type: ignore

    @classmethod
    def ready(cls) -> None:
        '''
        метод, отвечающий за иницилазацию получения всех NameSpace
        '''
        if not hasattr(cls, 'NAMESPACES'):
            cls._configure_namespace()
