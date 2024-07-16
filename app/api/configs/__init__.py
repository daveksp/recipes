from dependency_injector import containers
from dependency_injector import providers
#from sqlalchemy.ext.asyncio import create_async_engine

from app.extensions import db
from app.api.adapters.repositories.recipe_mysql import RecipeRepository
#from app.configs.settins import get_db_settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.api.adapters.entrypoints.rest.v1.recipe"])

    config = providers.Configuration()
    #config.from_dict(get_db_settings().model_dump())

    #db_engine = providers.Singleton(
    #    create_async_engine,
    #    config.get("db_dsn"),
    #    pool_size=config.get("db_max_pool_size"),
    #    max_overflow=config.get("db_overflow_size"),
    #    isolation_level="AUTOCOMMIT",
    #)

    recipe_port = providers.Factory(RecipeRepository, db_engine=db)