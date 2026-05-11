import os
from typing import List , Literal
from pydantic import BaseModel , Field
from langchain_core.output_parsers import PydanticOutputParser

class ClassifyModel(BaseModel):
    label: Literal["SPAM", "NOT SCAM]" ,"UNCERTAIN"]
    reasons: str
    risk_score: int = Field(..., ge=0, le=100, description="0..100 risk score")
    red_flags: str
    suggested_action: str

def get_parser():
    parser=PydanticOutputParser(pydantic_object=ClassifyModel)
    format_instructions=parser.get_format_instructions()
    return parser, format_instructions

