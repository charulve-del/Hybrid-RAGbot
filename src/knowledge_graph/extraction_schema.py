from typing import List, Optional

from pydantic import BaseModel, Field


class Entity(BaseModel):

    name: str

    entity_type: str

    description: Optional[str] = None


class Relationship(BaseModel):

    source: str

    source_type: str

    relationship: str

    target: str

    target_type: str


class KnowledgeGraphExtraction(BaseModel):

    entities: List[Entity] = Field(
        default_factory=list
    )

    relationships: List[Relationship] = Field(
        default_factory=list
    )