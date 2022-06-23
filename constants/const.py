from typing import Dict, List, Optional, Union

from .request import const as req_const
from .response import const as res_const


class ListOfConstants:
    def __init__(self, *constants: 'Constant'):
        self.constants: List['Constant'] = list(constants)

    def to_representation(self) -> List[Dict]:
        return [const.to_representation() for const in self.constants]    # type: ignore

    def convert_own_constants_type(self, to_response: bool) -> None:
        '''
        Если в схеме данные были заданы как ListOfConstants[Const, Const, ...], то нам нужно сконвертировать ошибки
        сначала в их частный вид

        @params to_response: bool - флаг, нужно ли нам их преобразовать в константы на response или на request
        '''
        if to_response:
            self.constants = list(map(lambda const: const.to_response_const(), self.constants))
        else:
            self.constants = list(map(lambda const: const.to_request_const(), self.constants))


class Constant:
    '''
    Оболочка над константами для дальнейшего разделения их по конкретным req_const.WithQuery, ...
    '''

    expected_data: Dict
    query_arg: Optional[Dict] = None
    comment: str = ''

    def __init__(self, expected_data: Dict, query_arg: Optional[Dict] = None, comment: str = ''):
        self.expected_data = expected_data
        self.query_arg = query_arg
        self.comment = comment

    def to_response_const(self) -> Union[res_const.WithoutQuery, res_const.WithQuery]:
        if self.query_arg is None:
            returned_const = res_const.WithoutQuery(
                expected_response_data=self.expected_data,
                comment=self.comment,
            )
        else:
            returned_const = res_const.WithQuery(
                expected_response_data=self.expected_data,
                query_arg=self.query_arg,
                comment=self.comment,
            )
        return returned_const

    def to_request_const(self) -> Union[req_const.WithoutQuery, req_const.WithQuery]:
        if self.query_arg is None:
            returned_const = req_const.WithoutQuery(
                expected_request_data=self.expected_data,
                comment=self.comment,
            )
        else:
            returned_const = req_const.WithQuery(
                expected_request_data=self.expected_data,
                query_arg=self.query_arg,
                comment=self.comment,
            )
        return returned_const
