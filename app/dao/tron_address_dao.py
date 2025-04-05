from app.dao.base import BaseDAO
from app.models.db.tron_address import TronAddress


class TronAddressDAO(BaseDAO):
    model = TronAddress
