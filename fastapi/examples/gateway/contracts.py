from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class DocumentIn(StrictModel):
    title: str = Field(min_length=1, max_length=120)
    text: str = Field(min_length=1, max_length=4096)

    @field_validator('title', 'text')
    @classmethod
    def visible(cls, value):
        if not value.strip() or '\x00' in value:
            raise ValueError('nonempty visible text required')
        return value


class DocumentOut(StrictModel):
    id: int
    title: str
    text: str
    version: int


class DocumentTitleIn(StrictModel):
    title: str = Field(min_length=1, max_length=120)

    @field_validator('title')
    @classmethod
    def title_visible(cls, value):
        if not value.strip() or '\x00' in value:
            raise ValueError('visible title required')
        return value


class JobIn(StrictModel):
    question: str = Field(min_length=1, max_length=300)
    document_ids: list[int] = Field(min_length=1, max_length=8)

    @field_validator('question')
    @classmethod
    def question_visible(cls, value):
        if not value.strip():
            raise ValueError('question required')
        return value

    @field_validator('document_ids')
    @classmethod
    def unique_ids(cls, value):
        if any(x <= 0 for x in value) or len(value) != len(set(value)):
            raise ValueError('positive unique IDs required')
        return sorted(value)


class Citation(StrictModel):
    document_id: int = Field(gt=0)
    start: int = Field(ge=0)
    end: int = Field(gt=0)
    quote: str = Field(min_length=1)


class Answer(StrictModel):
    status: Literal['answered', 'abstained']
    text: str = Field(min_length=1, max_length=8192)
    citations: list[Citation]


class JobOut(StrictModel):
    id: str
    state: Literal['queued', 'running', 'succeeded', 'failed', 'cancelled']
    attempt: int
    cancel_requested: bool
    result: Answer | None
