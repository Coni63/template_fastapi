from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from app.entities.todo import Todo


class Database:
    engine = create_async_engine("sqlite+aiosqlite:///database.sqlite")

    @staticmethod
    async def setup_db():
        async with Database.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    @staticmethod
    async def drop_db():
        async with Database.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    @staticmethod
    async def get_all_items() -> list[Todo]:
        async with AsyncSession(Database.engine) as session:
            query = await session.exec(select(Todo))
            return query.all()

    @staticmethod
    async def get_item_by_id(id: int) -> Todo | None:
        async with AsyncSession(Database.engine) as session:
            statement = select(Todo).where(Todo.id == id)
            query = await session.exec(statement)
            return query.first()

    @staticmethod
    async def create_item(item: Todo) -> int:
        async with AsyncSession(Database.engine) as session:
            session.add(item)
            await session.commit()
            await session.refresh(item)
            return item.id

    @staticmethod
    async def update_item(id: int, new_item: Todo):
        async with AsyncSession(Database.engine) as session:
            statement = (
                select(Todo)
                .where(Todo.id == id)
            )
            query = await session.exec(statement)
            item = query.one()
            item.title = new_item.title
            item.description = new_item.description
            item.state = new_item.state
            session.add(item)
            await session.commit()

    @staticmethod
    async def delete_item(id: int):
        async with AsyncSession(Database.engine) as session:
            statement = select(Todo).where(Todo.id == id)
            query = await session.exec(statement)
            element = query.one_or_none()
            if element is None:
                return 
            await session.delete(element)
            await session.commit()
