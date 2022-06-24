from django.apps import AppConfig

from ..adapters.initializers import NamespacesInitializer
from ..adapters.repositories import ViewsRepository
from ..schema_tool import SchemaTool


class ApywyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apywy'

    def ready(self) -> None:
        NamespacesInitializer.ready()
        views = ViewsRepository.all()
        SchemaTool.set_default_schema_data_to_views(views=views)
