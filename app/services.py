# app/services.py
from sqlalchemy.orm import Session
from . import models
from datetime import date
from typing import List
from sqlalchemy.exc import NoResultFound

# Matriculas
def criar_matricula(db: Session, nome: str, curso: str, data: date, status = models.StatusMatricula.ATIVA) -> models.Matricula:
    m = models.Matricula(nome=nome, curso=curso, data=data, status=status)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

def listar_matriculas(db: Session, skip: int = 0, limit: int = 100) -> List[models.Matricula]:
    return db.query(models.Matricula).offset(skip).limit(limit).all()

def obter_matricula(db: Session, matricula_id: int) -> models.Matricula | None:
    return db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()

def atualizar_matricula(db: Session, matricula_id: int, **fields) -> models.Matricula:
    m = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not m:
        raise NoResultFound(f"Matricula {matricula_id} não encontrada")
    for k, v in fields.items():
        if hasattr(m, k):
            setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return m

def remover_matricula(db: Session, matricula_id: int) -> None:
    m = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not m:
        raise NoResultFound(f"Matricula {matricula_id} não encontrada")
    db.delete(m)
    db.commit()

# Avaliacoes
def criar_avaliacao(db: Session, matricula_id: int, nota: float, tipo: models.TipoAvaliacao, data: date) -> models.Avaliacao:
    # valida se matrícula existe
    m = db.query(models.Matricula).filter(models.Matricula.id == matricula_id).first()
    if not m:
        raise NoResultFound(f"Matricula {matricula_id} não encontrada")
    a = models.Avaliacao(matricula_id=matricula_id, nota=nota, tipo=tipo, data=data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def listar_avaliacoes(db: Session, matricula_id: int | None = None, skip: int = 0, limit: int = 100):
    q = db.query(models.Avaliacao)
    if matricula_id is not None:
        q = q.filter(models.Avaliacao.matricula_id == matricula_id)
    return q.offset(skip).limit(limit).all()
