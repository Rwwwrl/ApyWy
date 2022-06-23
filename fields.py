import abc
from typing import Dict, List, Tuple

from .constants import exceptions
from .constants.const import Constant, ListOfConstants
from .utilities.custom_typing import AnyConst


class IField:
    @abc.abstractmethod
    def _pre_normalize_data(self, expected_data: AnyConst) -> ListOfConstants:
        raise NotImplementedError

    @abc.abstractmethod
    def to_representation(self) -> Dict:
        raise NotImplementedError


class StatusField(IField):
    '''
    Класс поля статуса HTTP метода.
    '''
    def __init__(self, expected_response_data: AnyConst):
        '''
        @param expected_response_data: Dict - значение ожидаемого словаря от бэкенда
        '''

        self.expected_response_data = self._pre_normalize_data(expected_response_data)
        self.response_status_code = None

    def _pre_normalize_data(self, expected_data: AnyConst) -> ListOfConstants:
        if isinstance(expected_data, dict):
            raise exceptions.NotValidResponseData(
                '''
                Больше использование expected_response_data не доступно, используйте Const.
                ''',
            )

        if isinstance(expected_data, Constant):
            expected_data = expected_data.to_response_const()
            return ListOfConstants(expected_data)

        if isinstance(expected_data, ListOfConstants):
            expected_data.convert_own_constants_type(to_response=True)
            return expected_data

    def to_representation(self) -> Dict:
        return {
            'expected_response_status_code': self.response_status_code,
            'expected_response_data': self.expected_response_data.to_representation(),
        }


class RequestDataField(IField):
    def __init__(self, expected_request_data: AnyConst):
        self.expected_request_data = self._pre_normalize_data(expected_data=expected_request_data)

    def _pre_normalize_data(self, expected_data: AnyConst) -> ListOfConstants:
        if isinstance(expected_data, dict):
            raise exceptions.NotValidRequestData(
                '''
                Больше использование expected_request_data не доступно, используйте Constant.
                ''',
            )
        if isinstance(expected_data, Constant):
            expected_data = expected_data.to_request_const()
            return ListOfConstants(expected_data)

        if isinstance(expected_data, ListOfConstants):
            expected_data.convert_own_constants_type(to_response=False)
            return expected_data

    def to_representation(self) -> Dict:
        return {
            'expected_request_data': self.expected_request_data.to_representation(),
        }


class MethodFieldMETA(type):
    '''
    TODO возможно его нужно сделать декоратором
    Метакласс, нужен лишь для добавления атрибута _http_statuses у BaseMethodField
    '''
    def __new__(cls, clsname: str, parents: Tuple, attrdict: Dict) -> 'MethodFieldMETA':

        http_statuses = []

        for key, attr in attrdict.items():
            if isinstance(attr, StatusField):
                # получаем статус код по имени атрибута
                response_status_code = key.split('_')[-1]
                attr.response_status_code = response_status_code

                http_statuses.append(attr)

        attrdict['_http_statuses'] = http_statuses

        return super().__new__(cls, clsname, parents, attrdict)


class MethodField(IField, metaclass=MethodFieldMETA):
    '''
    базовый класс HTTPField, нужный для сериализации
    '''
    @property
    def http_statuses(self) -> List['StatusField']:
        return self._http_statuses    # type: ignore

    def _representation_response_part(self) -> Dict:
        data: Dict = {'http_statuses': []}
        for http_status in self.http_statuses:
            data['http_statuses'].append(http_status.to_representation())    # type: ignore
        return data

    def _representation_request_part(self) -> Dict:
        expected_request_data = self.META.expected_request_data    # type: ignore
        if expected_request_data is not None:
            data = expected_request_data.to_representation()
        else:
            data = {'expected_request_data': None}
        return data

    def to_representation(self) -> Dict:
        '''
        По аналогию с drf, метод отвечающий за серилазацию поля
        '''
        response_part = self._representation_response_part()
        request_part = self._representation_request_part()
        return {**response_part, **request_part}

    class META:
        expected_request_data = None


class EmptyMethodField(IField):
    '''
    Поле пустого (не определенного разработчиком) HTTP метода. Нужен для присваивания в декораторе, ручками
    разработчик его навешивать не должен.
    '''
    def to_representation(self) -> Dict:
        return {'http_statuses': [], 'expected_request_data': None}
