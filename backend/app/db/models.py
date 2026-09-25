from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime
from enum import Enum
import sqlalchemy.dialects.postgresql as pg

class QuestType(str, Enum):
    main = "main"
    side = "side"
    gig = "gig"


class Quest(SQLModel, table=True):
    __tablename__ = "quests"
    
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    quest_type: QuestType = Field(nullable=False)
    wiki_url: str | None = Field(max_length=2048)

    progress: Progress | None = Relationship(back_populates="quest", uselist=False, sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self): 
        return f"<Quest {self.name}>"


class Progress(SQLModel, table=True):
    __tablename__ = "progress"

    id: int | None = Field(default=None, primary_key=True)
    quest_id: int = Field(foreign_key="quests.id", unique=True)
    completed: bool = Field(default=False, nullable=False) 
    notes: str | None = Field(default=None, max_length=2048)
    updated_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now)
    )  

    quest: Quest = Relationship(back_populates="progress", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self): 
        return f"<Progress {self.completed}>"