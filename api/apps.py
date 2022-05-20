from django.apps import AppConfig

from ..service_layer.initializers import NameSpacesInitializer, ViewsInitializer
from ..service_layer.schema_tool import SchemaTool


class ApywyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apywy'

    def ready(self) -> None:
        NameSpacesInitializer.ready()
        SchemaTool.set_default_schema_data_to_views(views=ViewsInitializer.VIEWS)    # type: ignore
