from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings
from app.models import Base, CrystalPrice


engine = create_async_engine(settings.DATABASE_URL, echo=False)

# async_sessionmaker из SQLAlchemy 2.0 решает проблему с варнингами PyCharm
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Создаёт таблицы в БД при первом запуске."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_last_price() -> CrystalPrice | None:
    """Возвращает последнюю записанную запись о ценах."""
    async with AsyncSessionLocal() as session:
        stmt = select(CrystalPrice).order_by(CrystalPrice.timestamp.desc()).limit(1)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def save_price(prices: dict[str, int]) -> None:
    """Сохраняет новые цены в базу данных."""
    async with AsyncSessionLocal() as session:
        new_price = CrystalPrice(
            green=prices.get("green", 0),
            blue=prices.get("blue", 0),
            red=prices.get("red", 0),
            violet=prices.get("violet", 0),
            white=prices.get("white", 0),
            cyan=prices.get("cyan", 0),
        )
        session.add(new_price)
        await session.commit()
