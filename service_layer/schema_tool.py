from typing import Dict, List

from . import entities, schema_fields
from ..utilities.custom_typing import DjangoView

ALL_HTTP_METHODS = set(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])


class SchemaTool:
    @staticmethod
    def set_default_schema_data_to_view_class(view_cls: DjangoView) -> None:
        '''
        Навесить на класс DjangoView дефолтные schema данные
        '''
        # нам не нужно навешивать дефолтную схему, если там уже весит схема (от декоратора).
        if hasattr(view_cls, '_schema_data'):
            return

        view_http_methods = filter(lambda attr_name: attr_name.upper() in ALL_HTTP_METHODS, view_cls.__dict__.keys())
        swagger_data = {
            'doc_string': view_cls.__doc__,
            'methods': {},
        }
        for http_method in view_http_methods:
            http_method = http_method.upper()
            schema_method_data = {
                'doc_string': getattr(view_cls, http_method.lower()).__doc__,
                'schema_data': schema_fields.EmptyHttpMethodField(),
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
            SchemaTool.set_default_schema_data_to_view_class(view_cls=view.view_class)
