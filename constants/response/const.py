import json
from dataclasses import dataclass
from typing import Dict


@dataclass
class Constant:
    '''
    Класс для обертки expected_response_data
    '''
    expected_response_data: Dict

    def to_representation(self) -> Dict:
        beautify_expected_response_data = json.dumps(self.expected_response_data, indent=4, ensure_ascii=False)
        return {
            'expected_response_data': beautify_expected_response_data,
            'query_arg': None,
        }


@dataclass
class WithQuery(Constant):
    query_arg: Dict

    def to_representation(self) -> Dict:
        data = super().to_representation()
        data['query_arg'] = self.query_arg
        return data


@dataclass
class WithoutQuery(Constant):
    pass
