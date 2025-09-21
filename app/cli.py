# app/cli.py
import click
from .db import get_engine, get_session_factory
from . import models, services, db as dbmod
from datetime import date
import os

engine = get_engine()
SessionLocal = get_session_factory(engine)
models.Base.metadata.create_all(bind=engine)

@click.group()
def cli():
    pass

@cli.command()
@click.option("--nome", prompt="Nome")
@click.option("--curso", prompt="Curso")
@click.option("--data", prompt="Data (YYYY-MM-DD)")
def criar_matricula_cmd(nome, curso, data):
    d = date.fromisoformat(data)
    with SessionLocal() as s:
        m = services.criar_matricula(s, nome=nome, curso=curso, data=d)
        click.echo(f"Matricula criada: {m.id} {m.nome} {m.curso}")

@cli.command()
def listar_matriculas_cmd():
    with SessionLocal() as s:
        ms = services.listar_matriculas(s)
        for m in ms:
            click.echo(f"{m.id}: {m.nome} | {m.curso} | {m.data} | {m.status}")

@cli.command()
@click.option("--matricula-id", type=int, prompt="ID da matrícula")
@click.option("--nota", type=float, prompt="Nota")
@click.option("--tipo", type=click.Choice(["PROVA","TRABALHO","RECUPERACAO"]))
@click.option("--data", prompt="Data (YYYY-MM-DD)")
def criar_avaliacao_cmd(matricula_id, nota, tipo, data):
    d = date.fromisoformat(data)
    from .models import TipoAvaliacao
    with SessionLocal() as s:
        a = services.criar_avaliacao(s, matricula_id=matricula_id, nota=nota, tipo=TipoAvaliacao(tipo), data=d)
        click.echo(f"Avaliação criada: {a.id} nota={a.nota} tipo={a.tipo}")

if __name__ == "__main__":
    cli()
