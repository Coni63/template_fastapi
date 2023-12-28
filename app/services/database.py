from sqlmodel import Session, SQLModel, create_engine, select
from app.entities.todo import Todo


class Database:
    engine = create_engine("sqlite:///database.sqlite")

    @staticmethod
    def setup_db():
        SQLModel.metadata.create_all(Database.engine)

    @staticmethod
    def drop_db():
        SQLModel.metadata.drop_all(Database.engine)

    @staticmethod
    def get_all_items() -> list[Todo]:
        with Session(Database.engine) as session:
            return session.exec(select(Todo)).all()

    @staticmethod
    def get_item_by_id(id: int) -> Todo | None:
        with Session(Database.engine) as session:
            statement = select(Todo).where(Todo.id == id)
            return session.exec(statement).first()

    @staticmethod
    def create_item(item: Todo) -> int:
        with Session(Database.engine) as session:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item.id

    @staticmethod
    def update_item(id: int, new_item: Todo):
        with Session(Database.engine) as session:
            statement = (
                select(Todo)
                .where(Todo.id == id)
            )
            item = session.exec(statement).one()
            item.title = new_item.title
            item.description = new_item.description
            item.state = new_item.state
            session.add(item)
            session.commit()

    @staticmethod
    def delete_item(id: int):
        with Session(Database.engine) as session:
            statement = select(Todo).where(Todo.id == id)
            element = session.exec(statement).first()

            session.delete(element)
            session.commit()
