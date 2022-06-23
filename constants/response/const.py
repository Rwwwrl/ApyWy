import json
from typing import Dict


class Constant:
    '''
    Класс для обертки expected_response_data
    '''
    expected_response_data: Dict
    comment: str

    def __init__(self, expected_response_data: Dict, comment: str = ''):
        self.expected_response_data = expected_response_data
        self.comment = comment

    def to_representation(self) -> Dict:
        beautify_expected_response_data = json.dumps(self.expected_response_data, indent=4, ensure_ascii=False)
        return {
            'expected_response_data': beautify_expected_response_data,
            'comment': self.comment,
            'query_arg': None,
        }


class WithQuery(Constant):
    query_arg: Dict

    def __init__(self, expected_response_data: Dict, query_arg: Dict, comment: str = ''):
        super().__init__(expected_response_data, comment)
        self.query_arg = query_arg

    def to_representation(self) -> Dict:
        data = super().to_representation()
        data['query_arg'] = self.query_arg
        return data


class WithoutQuery(Constant):
    pass
