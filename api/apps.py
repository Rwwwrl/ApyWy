from django.apps import AppConfig

from ..adapters.initializers import NamespacesInitializer, ViewsInitializer
from ..service_layer.schema_tool import SchemaTool


class ApywyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apywy'

    def ready(self) -> None:
        NamespacesInitializer.ready()
        views = ViewsInitializer.repository.all()    # type: ignore
        SchemaTool.set_default_schema_data_to_views(views=views)
