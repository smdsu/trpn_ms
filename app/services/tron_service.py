import tronpy


class TronService:
    def __init__(self):
        self.tron = tronpy.Tron()
    
    @staticmethod
    async def get_address_info(address: str) -> dict:
        try:
            tron = tronpy.Tron()
            # account = tron.get_account(address)
            balance = tron.get_account_balance(address)

            resources = tron.get_account_resource(address)
            bandwidth = resources.get("freeNetLimit", 0) - resources.get("freeNetUsed", 0)
            energy = resources.get("EnergyLimit", 0) - resources.get("EnergyUsed", 0)

            return {
                "balance": balance,
                "bandwidth": bandwidth,
                "energy": energy
            }
        except Exception as e:
            raise e
