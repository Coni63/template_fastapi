from pydantic import BaseModel


class Todo(BaseModel):
    id: int | None = None
    title: str
    description: str
    state: str
