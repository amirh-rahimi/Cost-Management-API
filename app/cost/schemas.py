from pydantic import BaseModel, Field
from typing import Annotated


OnlyLetters = Annotated[str, Field(pattern=r'^[A-Za-z\u0600-\u06FF\s]+$', max_length=500, min_length=1)]

class CostBase(BaseModel):
    description: OnlyLetters                                        
    amount: int


class ResponseCost(CostBase):
    id: int

    class Config:
        from_attributes = True

class CreateCost(CostBase):
    pass

#class EditCost(CostBase):
#    pass