from flask_sqlalchemy import SQLAlchemy
from jetkit.db import BaseQuery as JKBaseQuery, BaseModel as JKBaseModel, SQLA


class BaseQuery(JKBaseQuery):
    """Base class for queries."""


class BaseModel(JKBaseModel):
    """Base class to use for all models."""


db: SQLAlchemy = SQLA(model_class=BaseModel, query_class=BaseQuery)

# TODO: load all model classes
import ocp.model
