import typing
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
if typing.TYPE_CHECKING:
    from src.models import UserOrm

class VirtualMachineOrm(Base):
    __tablename__ = "virtual_machine"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    host: Mapped[str] = mapped_column(nullable=False)
    port: Mapped[int] = mapped_column(nullable=False)
    protocol: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)

    current_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),nullable=True)

    current_user: Mapped[Optional["UserOrm"]] = relationship(
        "UserOrm",
        back_populates="virtual_machine",
        foreign_keys=[current_user_id]
    )

    last_used_at: Mapped[datetime] = mapped_column(nullable=False)