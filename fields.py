import abc
from typing import Dict, List, Optional, Tuple, Union

from .constants.const import ListOfConstants
from .constants.request import const as req_const
from .constants.response import const as res_const
from .utilities.custom_typing import ResponseConst


class IField:
    @abc.abstractmethod
    def to_representation(self) -> Dict:
        raise NotImplementedError


class StatusField(IField):
    '''
    Класс поля статуса HTTP метода.
    '''
    def __init__(self, expected_response_data: Union[Dict, ResponseConst], comment: Optional[str] = None):
        '''
        @param expected_response_data: Dict - значение ожидаемого словаря от бэкенда
        @param comment: str - дополнительный комментарий по желанию
        '''
        if isinstance(expected_response_data, dict):
            expected_response_data = ListOfConstants(
                res_const.WithoutQuery(expected_response_data=expected_response_data),
            )

        if isinstance(expected_response_data, (res_const.WithoutQuery, res_const.WithQuery)):
            expected_response_data = ListOfConstants(expected_response_data)

        self.expected_response_data = expected_response_data
        self.comment = comment
        self.response_status_code = None

    def to_representation(self) -> Dict:
        return {
            'expected_response_status_code': self.response_status_code,
            'expected_response_data': self.expected_response_data.to_representation(),
            'comment': self.comment,
        }


class MethodFieldMETA(type):
    '''
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


class BaseMethodField(IField, metaclass=MethodFieldMETA):
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
            if isinstance(expected_request_data, dict):
                expected_request_data = ListOfConstants(
                    req_const.WithoutQuery(expected_request_data=expected_request_data),
                )
            if isinstance(expected_request_data, (req_const.WithoutQuery, req_const.WithQuery)):
                expected_request_data = ListOfConstants(expected_request_data)
            expected_request_data = expected_request_data.to_representation()

        data = {'expected_request_data': expected_request_data}
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


class MethodField(BaseMethodField, IField):
    '''
    Поле HTTP метода
    '''
    def to_representation(self) -> Dict:
        return super().to_representation()


class EmptyMethodField(BaseMethodField, IField):
    '''
    Поле пустого (не определенного разработчиком) HTTP метода. Нужен для присваивания в декораторе, ручками
    разработчик его навешивать не должен.
    '''
    def to_representation(self) -> Dict:
        return {'http_statuses': [], 'expected_request_data': None}
