# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum

class StatusMatricula(str, Enum):
    ATIVA = "ATIVA"
    TRANCADA = "TRANCADA"
    CANCELADA = "CANCELADA"

class TipoAvaliacao(str, Enum):
    PROVA = "PROVA"
    TRABALHO = "TRABALHO"
    RECUPERACAO = "RECUPERACAO"

class AvaliacaoCreate(BaseModel):
    matricula_id: int
    nota: float = Field(..., ge=0.0, le=10.0)
    tipo: TipoAvaliacao
    data: date

class AvaliacaoRead(BaseModel):
    id: int
    matricula_id: int
    nota: float
    tipo: TipoAvaliacao
    data: date

    class Config:
        orm_mode = True

class MatriculaCreate(BaseModel):
    nome: str
    curso: str
    data: date
    status: Optional[StatusMatricula] = StatusMatricula.ATIVA

class MatriculaRead(BaseModel):
    id: int
    nome: str
    curso: str
    data: date
    status: StatusMatricula
    avaliacoes: List[AvaliacaoRead] = []

    class Config:
        orm_mode = True
