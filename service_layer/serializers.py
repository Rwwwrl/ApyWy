import json
from typing import Dict, List

from .entities import NameSpace
from .schema_tool import SchemaTool


class BaseHTTPField:
    '''
    базовый класс HTTPField, нужный для сериализации
    '''
    def to_representation(self) -> Dict:
        '''
        По аналогию с drf, метод отвечающий за серилазацию поля
        '''
        expected_request_data = self.META.expected_request_data    # type: ignore
        if expected_request_data is not None:
            expected_request_data = json.dumps(expected_request_data, indent=4, ensure_ascii=False)

        data: Dict = {'http_statuses': [], 'expected_request_data': expected_request_data}
        return data

    class META:
        expected_request_data = None


class NameSpaceSerializer:
    '''
    Сериалайзер для namespace
    '''
    def __init__(self, namespaces: List[NameSpace]):
        result: Dict = {'namespaces': []}
        for namespace in namespaces:
            namespace_data = {}
            namespace_data['namespace_name'] = namespace.namespace_name
            namespace_data['views'] = []    # type: ignore
            for view in namespace.views:
                view_data = {}
                view_data['url_path'] = view.url_path._root + str(view.url_path)
                view_data['url_name'] = view.url_path.name
                schema_data = SchemaTool.get_schema_data_of_view_class(view_cls=view.view_class)
                view_data['doc_string'] = schema_data['doc_string']
                view_data['view_name'] = schema_data['view_name']
                view_data['view_methods'] = []    # type: ignore
                view_methods = schema_data['methods']
                for view_method in view_methods:
                    method_data = view_methods[view_method]
                    view_method_data = {}
                    view_method_data['HTTP_method'] = view_method
                    view_method_data['doc_string'] = method_data['doc_string']
                    view_method_data['http_data'] = method_data['schema_data'].to_representation()

                    view_data['view_methods'].append(view_method_data)    # type: ignore

                namespace_data['views'].append(view_data)    # type: ignore

            result['namespaces'].append(namespace_data)    # type: ignore

        self.data = result
