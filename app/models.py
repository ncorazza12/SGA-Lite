# app/models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Enum, DateTime, func
from sqlalchemy.orm import relationship
from .db import Base
import enum

class StatusMatricula(str, enum.Enum):
    ATIVA = "ATIVA"
    TRANCADA = "TRANCADA"
    CANCELADA = "CANCELADA"

class TipoAvaliacao(str, enum.Enum):
    PROVA = "PROVA"
    TRABALHO = "TRABALHO"
    RECUPERACAO = "RECUPERACAO"

class Matricula(Base):
    __tablename__ = "matriculas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    curso = Column(String(100), nullable=False)
    data = Column(Date, nullable=False)
    status = Column(Enum(StatusMatricula), nullable=False, default=StatusMatricula.ATIVA)

    avaliacoes = relationship("Avaliacao", back_populates="matricula", cascade="all, delete-orphan")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    matricula_id = Column(Integer, ForeignKey("matriculas.id", ondelete="CASCADE"), nullable=False)
    nota = Column(Float, nullable=False)
    tipo = Column(Enum(TipoAvaliacao), nullable=False)
    data = Column(Date, nullable=False)

    matricula = relationship("Matricula", back_populates="avaliacoes")
