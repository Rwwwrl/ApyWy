from typing import Callable

from .schema import Schema
from .schema_fields import EmptyHttpMethodField
from .schema_tool import SchemaTool
from ..utilities.custom_typing import DjangoView


def set_apywy_schema(schema: Schema) -> Callable:
    '''
    Декоратор, который навешивает schema на DjangoView при ее инициализации
    '''
    def inner(view_cls: DjangoView) -> DjangoView:
        # декоратор срабатывает раньше чем apps.ready, поэтому нам нужно навешивать
        # дефолтную схему самостоятельно
        SchemaTool.set_default_schema_data_to_view_class(view_cls=view_cls)

        schema_data = SchemaTool.get_schema_data_of_view_class(view_cls=view_cls)

        for method_schema_data in schema_data['methods']:
            schema_data_class = getattr(
                schema,
                method_schema_data,
                EmptyHttpMethodField,
            )

            schema_data['methods'][method_schema_data]['schema_data'] = schema_data_class()
            return view_cls

    return inner
