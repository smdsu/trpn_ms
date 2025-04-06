import fastapi

from tronpy.exceptions import AddressNotFound

from fastapi_pagination import Page, paginate

from app.dao.tron_address_dao import TronAddressDAO
from app.services.tron_service import TronService

from app.models.schemas.tron_address import STronAddress

router = fastapi.APIRouter(prefix="/tron", tags=["tron"])


@router.post("/get-address-info", response_model=STronAddress)
async def get_address_info(address: str) -> STronAddress:
    try:
        address_info = await TronService.get_address_info(address)
        await TronAddressDAO.add(address=address, **address_info)
        address_info['address'] = address
        return address_info
    except AddressNotFound:
        raise fastapi.HTTPException(status_code=404, detail=f'Address not found: {address}')
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=f'Error getting address info: {str(e)}')
    

@router.get("/get-all-addresses", response_model=Page[STronAddress])
async def get_all_addresses() -> Page[STronAddress]:
    addresses = await TronAddressDAO.find_all()
    return paginate(addresses)
