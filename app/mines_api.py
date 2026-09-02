import httpx
from yarl import URL

from app.config import settings


class MinesAPIClient:
    """Клиент для взаимодействия с API игры Mines 4."""
    
    def __init__(self) -> None:
        self.base_url = URL("https://mines3.firetype.ru/api/public")
        self.headers = {
            "Authorization": f"Bearer {settings.MINES_API_TOKEN}",
            "Accept": "*/*",
        }
        self.timeout = 10.0
        # Используем настройку напрямую из Pydantic Settings
        self.verify_ssl = settings.API_VERIFY_SSL
    
    async def get_crystal_prices(self) -> dict[str, int]:
        """Получает актуальные цены на кристаллы из API."""
        url = str(self.base_url / "CrystalPrices")
        async with httpx.AsyncClient(verify=self.verify_ssl) as client:
            response = await client.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()


mines_api = MinesAPIClient()
