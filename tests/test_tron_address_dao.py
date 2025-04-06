import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy.exc import SQLAlchemyError

from app.dao.tron_address_dao import TronAddressDAO
from app.models.db.tron_address import TronAddress


@pytest.mark.asyncio
async def test_tron_address_add():
    """
    Unit test for the add method in TronAddressDAO.
    Checks that the data is correctly added to the database.
    """
    test_address = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
    test_balance = 1000000
    test_bandwidth = 5000
    test_energy = 2000

    result_obj = TronAddress()
    result_obj.address = test_address
    result_obj.balance = test_balance
    result_obj.bandwidth = test_bandwidth
    result_obj.energy = test_energy

    with patch('app.dao.base.BaseDAO.add',
               new=AsyncMock(return_value=result_obj)) as mock_add:
        result = await TronAddressDAO.add(
            address=test_address,
            balance=test_balance,
            bandwidth=test_bandwidth,
            energy=test_energy
        )

        mock_add.assert_called_once_with(
            address=test_address,
            balance=test_balance,
            bandwidth=test_bandwidth,
            energy=test_energy
        )

        assert result == result_obj
        assert result.address == test_address
        assert result.balance == test_balance
        assert result.bandwidth == test_bandwidth
        assert result.energy == test_energy


@pytest.mark.asyncio
async def test_tron_address_add_failure():
    """
    Unit test for the add method in TronAddressDAO.
    Checks that the data is correctly added to the database.
    """
    test_address = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
    test_balance = 1000000
    test_bandwidth = 5000
    test_energy = 2000

    with patch('app.dao.base.BaseDAO.add',
               new=AsyncMock(
                   side_effect=SQLAlchemyError("DB Error")
                   )) as mock_add:
        with pytest.raises(Exception):
            await TronAddressDAO.add(
                address=test_address,
                balance=test_balance,
                bandwidth=test_bandwidth,
                energy=test_energy
            )

        mock_add.assert_called_once_with(
            address=test_address,
            balance=test_balance,
            bandwidth=test_bandwidth,
            energy=test_energy
        )
