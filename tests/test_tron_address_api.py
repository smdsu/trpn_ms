import pytest
from unittest.mock import patch

from app.services.tron_service import TronService
from app.models.db.tron_address import TronAddress
from app.dao.tron_address_dao import TronAddressDAO


@pytest.mark.asyncio
async def test_get_address_info_endpoint(client):
    """
    /tron/get-address-info.
    A case where the address does not yet exist in the database and is
    obtained via TronService.
    """
    address_info = {
        "balance": 1000000,
        "bandwidth": 5000,
        "energy": 2000
    }

    test_address = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"

    async def mock_get_address_info_impl(address):
        return address_info

    async def mock_find_one_or_none_impl(**kwargs):
        return None

    async def mock_add_impl(**kwargs):
        tron_address = TronAddress()
        tron_address.address = kwargs.get('address')
        tron_address.balance = kwargs.get('balance')
        tron_address.bandwidth = kwargs.get('bandwidth')
        tron_address.energy = kwargs.get('energy')
        return tron_address

    with patch.object(
            TronService,
            "get_address_info",
            side_effect=mock_get_address_info_impl
            ), patch.object(
                TronAddressDAO,
                "find_one_or_none_by_filter",
                side_effect=mock_find_one_or_none_impl
                ), patch.object(
                    TronAddressDAO,
                    "add",
                    side_effect=mock_add_impl
                ):
        response = client.post(
            f"/api/tron/get-address-info?address={test_address}"
        )
        assert response.status_code == 200
        response_data = response.json()

        assert response_data["address"] == test_address
        assert response_data["balance"] == address_info["balance"]
        assert response_data["bandwidth"] == address_info["bandwidth"]
        assert response_data["energy"] == address_info["energy"]


@pytest.mark.asyncio
async def test_get_address_info_endpoint_existing(client):
    """
    /tron/get-address-info.
    A case where the address already exists in the database.
    """
    test_address = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"

    db_address = TronAddress()
    db_address.id = 1
    db_address.address = test_address
    db_address.balance = 1000000
    db_address.bandwidth = 5000
    db_address.energy = 2000

    async def mock_find_one_or_none_impl(**kwargs):
        if kwargs.get('address') == test_address:
            return db_address
        return None

    with patch.object(
            TronAddressDAO,
            "find_one_or_none_by_filter",
            side_effect=mock_find_one_or_none_impl
            ), patch.object(
                TronService,
                "get_address_info"
            ) as mock_get_address_info:

        response = client.post(
            f"/api/tron/get-address-info?address={test_address}"
        )

        mock_get_address_info.assert_not_called()

        assert response.status_code == 200
        response_data = response.json()

        assert response_data["address"] == db_address.address
        assert response_data["balance"] == db_address.balance
        assert response_data["bandwidth"] == db_address.bandwidth
        assert response_data["energy"] == db_address.energy
