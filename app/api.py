# app/api.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import db, models, services, schemas
import uvicorn
from datetime import date

engine = db.get_engine()
SessionLocal = db.get_session_factory(engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGA Lite")

def get_db():
    dbs = SessionLocal()
    try:
        yield dbs
    finally:
        dbs.close()

# Matriculas
@app.post("/matriculas/", response_model=schemas.MatriculaRead)
def api_criar_matricula(payload: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    m = services.criar_matricula(db, nome=payload.nome, curso=payload.curso, data=payload.data, status=payload.status)
    return m

@app.get("/matriculas/", response_model=list[schemas.MatriculaRead])
def api_listar_matriculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.listar_matriculas(db, skip=skip, limit=limit)

@app.get("/matriculas/{matricula_id}", response_model=schemas.MatriculaRead)
def api_obter_matricula(matricula_id: int, db: Session = Depends(get_db)):
    m = services.obter_matricula(db, matricula_id)
    if not m:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return m

@app.put("/matriculas/{matricula_id}", response_model=schemas.MatriculaRead)
def api_atualizar_matricula(matricula_id: int, payload: schemas.MatriculaCreate, db: Session = Depends(get_db)):
    try:
        m = services.atualizar_matricula(db, matricula_id, nome=payload.nome, curso=payload.curso, data=payload.data, status=payload.status)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return m

@app.delete("/matriculas/{matricula_id}", status_code=204)
def api_remover_matricula(matricula_id: int, db: Session = Depends(get_db)):
    try:
        services.remover_matricula(db, matricula_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return

# Avaliacoes
@app.post("/avaliacoes/", response_model=schemas.AvaliacaoRead)
def api_criar_avaliacao(payload: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    try:
        a = services.criar_avaliacao(db, matricula_id=payload.matricula_id, nota=payload.nota, tipo=payload.tipo, data=payload.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return a

@app.get("/avaliacoes/", response_model=list[schemas.AvaliacaoRead])
def api_listar_avaliacoes(matricula_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.listar_avaliacoes(db, matricula_id=matricula_id, skip=skip, limit=limit)

# Run: uvicorn app.api:app --reload
if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8000, reload=True)
