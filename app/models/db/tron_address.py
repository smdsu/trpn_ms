from sqlalchemy.orm import Mapped

from app.models.db.base import Base, int_pk


class TronAddress(Base):
    __tablename__ = "tron_addresses"

    id: Mapped[int_pk]
    address: Mapped[str]
    bandwidth: Mapped[int]
    energy: Mapped[int]
    balance: Mapped[float]

    def __repr__(self) -> str:
        return f"<TronAddress({self.address})>"

