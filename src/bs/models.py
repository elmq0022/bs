from typing import Optional


from sqlmodel import (
    Field,
    SQLModel,
    Column,
    func,
    DateTime,
)

from pydantic import ConfigDict

import datetime
import uuid


class Article(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    body: str
    created_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc),
    )
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(DateTime(), onupdate=func.now())
    )

    model_config = ConfigDict(validate_assignment=True)
