from sqlalchemy.orm import DeclarativeBase

"""
    This class only exists to provide support for the ORM functions implemented with SQLAlchemy and SHOULD NOT be utilized otherwise.
"""
class Base(DeclarativeBase):
    pass