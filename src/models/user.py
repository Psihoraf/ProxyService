import typing
from  datetime import datetime
from typing import Optional

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if typing.TYPE_CHECKING:
    from src.models.virtual_machine import VirtualMachineOrm


class UserOrm(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
    activation_key: Mapped[Optional[str]] = mapped_column(unique=True, nullable=True)
    activation_key_expires: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    virtual_machines: Mapped[list["VirtualMachineOrm"]] = relationship(
        "VirtualMachineOrm",
        back_populates="current_user",
        foreign_keys="VirtualMachineOrm.current_user_id"
    )
