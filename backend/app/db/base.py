from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# predictable constraint names, so later migrations can find and drop them by name.
NAME_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


# create a base class for the database models.
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAME_CONVENTION)
