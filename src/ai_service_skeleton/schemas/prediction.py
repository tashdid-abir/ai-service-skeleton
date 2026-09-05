from typing import Annotated, Literal

from pydantic import BaseModel, Field, field_validator


PredictionLabel = Literal["positive", "negative", "neutral"]

class PredictionRequest(BaseModel):
    text: Annotated[
        str,
        Field(
            min_length=1,
            max_length=2_000,
            description="Text that will be classified",
        ),
    ]

    @field_validator("text")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        normalized_text = value.strip()

        if normalized_text.isdigit():
            raise ValueError("text must contain words, not only digits")

        if not normalized_text:
            raise ValueError("text must not be empty or whitespace only")

        return normalized_text

class PredictionResponse(BaseModel):
    label: PredictionLabel

    confidence: Annotated[
        float,
        Field(ge=0.0, le=1.0),
    ]

    predictor_id: Annotated[
        str,
        Field(min_length=1),
    ]