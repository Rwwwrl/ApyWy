from typing import Dict, List, Optional, Tuple, Union

from .constants_types import ListOfConstants, WithQuery, WithoutQuery
from .service_layer.serializers import BaseHTTPField


class HttpMethodFieldMETA(type):
    '''
    TODO возможно его стоит переписать в декоратор
    Метакласс, нужен лишь для добавления атрибута _http_statuses у DefaulHttpMethodField
    '''
    def __new__(cls, clsname: str, parents: Tuple, attrdict: Dict) -> 'HttpMethodFieldMETA':

        http_statuses = []

        for key, attr in attrdict.items():
            if isinstance(attr, HttpStatusField):
                # получить статус код по имени атрибута
                response_status_code = key.split('_')[-1]
                attr.response_status_code = response_status_code

                http_statuses.append(attr)

        attrdict['_http_statuses'] = http_statuses

        return super().__new__(cls, clsname, parents, attrdict)


class HttpStatusField:
    '''
    Класс поля статуса HTTP метода.
    '''
    def __init__(
        self,
        expected_response_data: Union[Dict, WithoutQuery, WithQuery, ListOfConstants],
        comment: Optional[str] = None,
    ) -> None:
        '''
        @param expected_response_data: Dict - значение ожидаемого словаря от бэкенда
        @param commnent: str - дополнительный комментарий по желанию
        '''
        if isinstance(expected_response_data, dict):
            expected_response_data = ListOfConstants(WithoutQuery(expected_response_data=expected_response_data))

        if isinstance(expected_response_data, (WithoutQuery, WithQuery)):
            expected_response_data = ListOfConstants(expected_response_data)

        self.expected_response_data = expected_response_data
        self.comment = comment
        self.response_status_code = None

    def to_representation(self) -> Dict:
        '''
        По аналогию с drf, метод отвечающий за серилазацию поля
        '''
        return {
            'expected_response_status_code': self.response_status_code,
            'expected_response_data': self.expected_response_data.to_representation(),
            'comment': self.comment,
        }


class HttpMethodField(BaseHTTPField, metaclass=HttpMethodFieldMETA):
    '''
    Поле HTTP метода
    '''
    @property
    def http_statuses(self) -> List[HttpStatusField]:
        return self._http_statuses    # type: ignore

    def to_representation(self) -> Dict:
        data = super().to_representation()
        for http_status in self.http_statuses:
            data['http_statuses'].append(http_status.to_representation())    # type: ignore
        return data


class EmptyHttpMethodField(BaseHTTPField):
    '''
    Поле пустого (не определенного разработчиком) HTTP метода. Нужен для присваивания в декораторе, ручками
    разработчик его навешивать не должен.
    '''
    pass
