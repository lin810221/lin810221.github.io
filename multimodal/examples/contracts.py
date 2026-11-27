"""Strict extraction schema and business constraints are separate from generation."""
from datetime import date
from decimal import Decimal,InvalidOperation
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,model_validator
from geometry import box

class Evidence(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    page_index:int=Field(ge=0)
    bbox:list[float]
    quote:str=Field(min_length=1)
    @model_validator(mode='after')
    def valid_box(self):box(self.bbox);return self

class Invoice(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    document_sha256:str=Field(pattern=r'^[a-f0-9]{64}$')
    invoice_no:str=Field(pattern=r'^DW-\d{4}-\d{3}$')
    invoice_date:str
    currency:Literal['USD']
    subtotal_cents:int=Field(ge=0)
    tax_cents:int=Field(ge=0)
    total_cents:int=Field(ge=0)
    evidence:dict[str,Evidence]
    @model_validator(mode='after')
    def reconcile(self):
        date.fromisoformat(self.invoice_date)
        if self.subtotal_cents+self.tax_cents!=self.total_cents:raise ValueError('Subtotal plus tax must equal total')
        required={'invoice_no','invoice_date','currency','subtotal_cents','tax_cents','total_cents'}
        if set(self.evidence)!=required:raise ValueError('Each extracted field needs evidence')
        return self

def cents(raw):
    if not isinstance(raw,str):raise ValueError('Decimal text required')
    try:value=Decimal(raw)
    except InvalidOperation:raise ValueError('Invalid decimal') from None
    if not value.is_finite() or value<0 or value.as_tuple().exponent < -2:raise ValueError('Nonnegative amount with at most two decimals required')
    return int(value*100)

def decide(known,valid_evidence,reconciled,score,threshold=.9):
    if not 0<=score<=1 or not 0<=threshold<=1:raise ValueError('Invalid review threshold')
    if not known:return 'unknown'
    return 'accept' if valid_evidence and reconciled and score>=threshold else 'review'
