from typing import Dict, List

from . import entities
from ..utilities.custom_typing import DjangoView

ALL_HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']


class SchemaTool:
    @staticmethod
    def _check_view_has_method_attr(view_cls: DjangoView, http_method: str) -> bool:
        '''
        функция для проверки наличия у DjangoView http метода
        '''
        return hasattr(view_cls, http_method)

    @staticmethod
    def set_default_schema_data_to_view_class(view_cls: DjangoView) -> None:
        '''
        Навесить на класс DjangoView дефолтные schema данные
        '''
        from .. import fields

        # нам не нужно навешивать дефолтную схему, если там уже весит схема (от декоратора).
        if hasattr(view_cls, '_schema_data'):
            return

        view_http_methods = filter(
            lambda http_method: SchemaTool.
            _check_view_has_method_attr(view_cls=view_cls, http_method=http_method.lower()),
            ALL_HTTP_METHODS,
        )
        swagger_data = {
            'doc_string': view_cls.__doc__,
            'view_name': view_cls.__name__,
            'methods': {},
        }
        for http_method in view_http_methods:
            http_method = http_method.upper()
            schema_method_data = {
                'doc_string': getattr(view_cls, http_method.lower()).__doc__,
                'schema_data': fields.EmptyHttpMethodField(),
            }
            swagger_data['methods'][http_method] = schema_method_data
        view_cls._schema_data = swagger_data

    @staticmethod
    def get_schema_data_of_view_class(view_cls: DjangoView) -> Dict:
        '''
        Получить данные schema из класса View
        '''
        return view_cls._schema_data

    @staticmethod
    def set_default_schema_data_to_views(views: List[entities.View]) -> None:
        '''
        Навесить дефолтные данные schema на все view во views
        '''
        for view in views:
            SchemaTool.set_default_schema_data_to_view_class(view_cls=view.django_view_class)
