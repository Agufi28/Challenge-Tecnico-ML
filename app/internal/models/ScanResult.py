from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from internal.models.Base import Base
from internal.models.Control import Control
from internal.models.DatabaseSchema import DatabaseSchema
from internal.models.User import User
class ScanResult(Base):
    __tablename__ = "scan_result"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    executed_on: Mapped[datetime] = mapped_column(default=datetime.now())
    database_id: Mapped[int] = mapped_column(ForeignKey("databases.id"))

    schemas: Mapped[list[DatabaseSchema]] = relationship(cascade="all, delete-orphan")
    database: Mapped['DatabaseMetadataAdapter'] = relationship(back_populates="scans") # type: ignore

    requested_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    requestedBy: Mapped[Optional[User]] = relationship()

    def __init__(self, database: 'DatabaseMetadataAdapter'): # type: ignore
        self.database = database

    def run(self, controls:list[Control]):
        for schema in self.schemas:
            schema.run(controls)
