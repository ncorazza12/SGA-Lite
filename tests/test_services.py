# tests/test_services.py
from app.db import get_engine, get_session_factory
from app import models
from app import services
from datetime import date
import tempfile
import os

def setup_in_memory_db():
    url = "sqlite:///:memory:"
    engine = get_engine(url)
    SessionLocal = get_session_factory(engine)
    models.Base.metadata.create_all(bind=engine)
    return SessionLocal

def test_criar_listar_matricula():
    SessionLocal = setup_in_memory_db()
    with SessionLocal() as s:
        m = services.criar_matricula(s, nome="João Silva", curso="Engenharia", data=date(2024,1,10))
        assert m.id is not None
        ms = services.listar_matriculas(s)
        assert len(ms) == 1

def test_criar_avaliacao_para_matricula():
    SessionLocal = setup_in_memory_db()
    with SessionLocal() as s:
        m = services.criar_matricula(s, nome="Maria", curso="Direito", data=date(2023,7,1))
        a = services.criar_avaliacao(s, matricula_id=m.id, nota=8.5, tipo=models.TipoAvaliacao.PROVA, data=date(2024,6,1))
        avals = services.listar_avaliacoes(s, matricula_id=m.id)
        assert len(avals) == 1
        assert abs(avals[0].nota - 8.5) < 0.001
