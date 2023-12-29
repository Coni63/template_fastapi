from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.entities.todo import Todo


class Database:
    _instance = None

    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///database.sqlite")
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    def __new__(cls):
        if cls._instance is not None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    async def setup_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def drop_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    async def get_all_items(self) -> list[Todo]:
        async with self.async_session() as session:
            query = await session.execute(select(Todo))
            return query.scalars().all()

    async def get_item_by_id(self, id: int) -> Todo | None:
        async with self.async_session() as session:
            statement = select(Todo).where(Todo.id == id)
            query = await session.execute(statement)
            return query.scalars().one()

    async def create_item(self, item: Todo) -> int:
        async with self.async_session() as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return item.id

    async def update_item(self, id: int, new_item: Todo):
        async with self.async_session() as session:
            statement = (
                select(Todo)
                .where(Todo.id == id)
            )
            query = await session.execute(statement)
            item = query.scalars().one()
            item.title = new_item.title
            item.description = new_item.description
            item.state = new_item.state
            session.add(item)
            await session.commit()

    async def delete_item(self, id: int):
        async with self.async_session() as session:
            statement = select(Todo).where(Todo.id == id)
            query = await session.execute(statement)
            element = query.scalar_one_or_none()
            if element is None:
                return
            await session.delete(element)
            await session.commit()
